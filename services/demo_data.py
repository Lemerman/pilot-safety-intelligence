#!/usr/bin/env python
"""Generate demo data with detailed timing instrumentation - SMOKE TEST VERSION"""
import sys
import os
import time
from datetime import datetime, timedelta
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def log_time(section, elapsed):
    print(f"  [{section}] {elapsed:.3f}s")

class DemoDataGenerator:
    """Generate demo data with profiling"""
    
    def __init__(self, num_sessions=5):
        t0 = time.perf_counter()
        from models.base import SessionLocal
        self.session = SessionLocal()
        t1 = time.perf_counter()
        log_time("SessionLocal init", t1 - t0)
        
        self.pilots = []
        self.evaluators = []
        self.competencies = []
        self.num_sessions = num_sessions
        
    def generate_all(self):
        """Generate complete demo dataset"""
        total_start = time.perf_counter()
        
        try:
            print("\n" + "="*70)
            print(f"GENERATING DEMO DATA WITH PROFILING ({self.num_sessions} sessions)")
            print("="*70)
            
            # Section 1: Load models
            t0 = time.perf_counter()
            from models import (
                Pilot, PilotRole, Evaluator, EvaluatorType,
                Competency, CompetencyCode,
                AssessmentSession, AssessmentType, PhaseOfFlight, PFPMRole,
                Event, Threat, Error, UndesiredAircraftState, Countermeasure,
                CompetencyAssessment
            )
            t1 = time.perf_counter()
            print(f"\n[IMPORTS] {t1 - t0:.3f}s")
            
            # Section 2: Generate pilots
            t0 = time.perf_counter()
            self.generate_pilots()
            t1 = time.perf_counter()
            print(f"[PILOTS] {t1 - t0:.3f}s")
            
            # Section 3: Generate evaluators
            t0 = time.perf_counter()
            self.generate_evaluators()
            t1 = time.perf_counter()
            print(f"[EVALUATORS] {t1 - t0:.3f}s")
            
            # Section 4: Generate sessions and TEM data
            t0 = time.perf_counter()
            self.generate_assessment_sessions(
                Pilot, Evaluator, Competency, CompetencyCode,
                AssessmentSession, AssessmentType, PhaseOfFlight, PFPMRole,
                Event, Threat, Error, UndesiredAircraftState, Countermeasure,
                CompetencyAssessment
            )
            t1 = time.perf_counter()
            print(f"[SESSIONS & TEM] {t1 - t0:.3f}s")
            
            # Query final counts
            t0 = time.perf_counter()
            self.print_record_counts()
            t1 = time.perf_counter()
            print(f"[QUERY COUNTS] {t1 - t0:.3f}s")
            
            total_elapsed = time.perf_counter() - total_start
            print("\n" + "="*70)
            print(f"✓ TOTAL TIME: {total_elapsed:.3f}s")
            print("="*70)
            
        except Exception as e:
            print(f"\n✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        finally:
            self.session.close()
    
    def print_record_counts(self):
        """Query and print record counts"""
        from models import (
            Pilot, Evaluator, Competency, AssessmentSession, Event,
            Threat, Error, UndesiredAircraftState, Countermeasure, CompetencyAssessment
        )
        
        print("\nRECORD COUNTS:")
        print(f"  Pilots: {self.session.query(Pilot).count()}")
        print(f"  Evaluators: {self.session.query(Evaluator).count()}")
        print(f"  Competencies: {self.session.query(Competency).count()}")
        print(f"  AssessmentSessions: {self.session.query(AssessmentSession).count()}")
        print(f"  Events: {self.session.query(Event).count()}")
        print(f"  Threats: {self.session.query(Threat).count()}")
        print(f"  Errors: {self.session.query(Error).count()}")
        print(f"  UndesiredAircraftStates: {self.session.query(UndesiredAircraftState).count()}")
        print(f"  Countermeasures: {self.session.query(Countermeasure).count()}")
        print(f"  CompetencyAssessments: {self.session.query(CompetencyAssessment).count()}")
    
    def generate_pilots(self):
        """Generate 20 pilots"""
        print("\nGenerating pilots...")
        from models import Pilot, PilotRole
        
        roles = [PilotRole.CAPTAIN, PilotRole.FIRST_OFFICER]
        
        t0 = time.perf_counter()
        for i in range(20):
            pilot = Pilot(
                pilot_code=f"PLT{1000+i}",
                role=random.choice(roles),
                aircraft_type="A320",
                fleet="Mainline",
                active=1
            )
            self.session.add(pilot)
            self.pilots.append(pilot)
        t1 = time.perf_counter()
        log_time("add 20 pilots", t1 - t0)
        
        t0 = time.perf_counter()
        self.session.commit()
        t1 = time.perf_counter()
        log_time("commit pilots", t1 - t0)
        
        print(f"✓ Created {len(self.pilots)} pilots")
    
    def generate_evaluators(self):
        """Generate 5 evaluators"""
        print("\nGenerating evaluators...")
        from models import Evaluator, EvaluatorType
        
        evaluator_types = [
            EvaluatorType.TRE, EvaluatorType.SIM, EvaluatorType.LTC,
            EvaluatorType.CHIEF, EvaluatorType.MANAGER
        ]
        evaluator_names = ["Evaluator A", "Evaluator B", "Evaluator C", "Evaluator D", "Evaluator E"]
        
        t0 = time.perf_counter()
        for i, (ev_type, name) in enumerate(zip(evaluator_types, evaluator_names)):
            evaluator = Evaluator(
                evaluator_code=f"EVL{100+i}",
                name=name,
                evaluator_type=ev_type,
                aircraft_type="A320",
                active=1
            )
            self.session.add(evaluator)
            self.evaluators.append(evaluator)
        t1 = time.perf_counter()
        log_time("add evaluators", t1 - t0)
        
        t0 = time.perf_counter()
        self.session.commit()
        t1 = time.perf_counter()
        log_time("commit evaluators", t1 - t0)
        
        print(f"✓ Created {len(self.evaluators)} evaluators")
    
    def generate_assessment_sessions(self, Pilot, Evaluator, Competency, CompetencyCode,
                                    AssessmentSession, AssessmentType, PhaseOfFlight, PFPMRole,
                                    Event, Threat, Error, UndesiredAircraftState, Countermeasure,
                                    CompetencyAssessment):
        """Generate N sessions with full TEM data"""
        print(f"\nGenerating {self.num_sessions} assessment sessions...")
        
        # Query competencies ONCE
        t0 = time.perf_counter()
        competencies = self.session.query(Competency).all()
        t1 = time.perf_counter()
        log_time("query competencies", t1 - t0)
        print(f"  Loaded {len(competencies)} competencies")
        
        # Cache enum values
        t0 = time.perf_counter()
        assessment_types = list(AssessmentType)
        phases = list(PhaseOfFlight)
        pf_pm_roles = list(PFPMRole)
        comp_codes = [c.name for c in CompetencyCode]
        t1 = time.perf_counter()
        log_time("cache enums", t1 - t0)
        
        # Session generation loop with per-session timing
        session_loop_start = time.perf_counter()
        session_count = 0
        
        for session_num in range(self.num_sessions):
            session_start = time.perf_counter()
            
            pilot = random.choice(self.pilots)
            evaluator = random.choice(self.evaluators)
            days_ago = random.randint(1, 90)
            session_date = datetime.utcnow() - timedelta(days=days_ago)
            
            session = AssessmentSession(
                pilot_id=pilot.pilot_id,
                evaluator_id=evaluator.evaluator_id,
                assessment_type=random.choice(assessment_types),
                aircraft_type="A320",
                fleet="Mainline",
                assessment_date=session_date,
                training_module=random.choice(["Type Rating", "Recurrent", "Proficiency", "Line Training"]),
                scenario_event=random.choice(["Normal Operation", "Engine Failure", "Weather Challenge", "Systems Failure"]),
                pf_pm_role=random.choice(pf_pm_roles),
                phase_of_flight=random.choice(phases),
                comments=random.choice(["Standard session", "Challenging conditions", "Excellent performance", None])
            )
            self.session.add(session)
            self.session.flush()
            
            # Events and TEM
            for _ in range(random.randint(1, 3)):
                event = Event(
                    session_id=session.session_id,
                    event_description=random.choice(["Normal cruise", "Approach phase", "Emergency scenario", "System management"]),
                    phase_of_flight=random.choice(phases)
                )
                self.session.add(event)
                self.session.flush()
                
                if random.random() > 0.3:
                    self.session.add(Threat(
                        event_id=event.event_id,
                        threat_description=random.choice(["Thunderstorm", "Engine issue", "ATC", "Fatigue", "Runway"]),
                        threat_type=random.choice(["Weather", "Aircraft Malfunction", "ATC Instruction", "Fatigue", "Runway Condition"])
                    ))
                
                if random.random() > 0.5:
                    self.session.add(Error(
                        event_id=event.event_id,
                        error_description=random.choice(["Forgot flaps", "Missed callout", "Wrong altitude", "Control deviation", "Incomplete checklist"]),
                        error_type=random.choice(["Procedural Error", "Communication Error", "Navigation Error", "Control Error", "Checklist Error"])
                    ))
                
                if random.random() > 0.6:
                    self.session.add(UndesiredAircraftState(
                        event_id=event.event_id,
                        state_description=random.choice(["Alt +200ft", "Speed +5kt", "Heading +3°", "Descent +100fpm"]),
                        state_type=random.choice(["Altitude Deviation", "Speed Deviation", "Heading Deviation", "Descent Rate Deviation"])
                    ))
                
                if random.random() > 0.4:
                    self.session.add(Countermeasure(
                        event_id=event.event_id,
                        countermeasure_description="Effective crew coordination",
                        countermeasure_type=random.choice(["Technical", "Procedural", "CRM", "Automation"]),
                        competency_involved=random.choice(comp_codes),
                        effectiveness=random.choice(["Effective", "Partially Effective", "Ineffective"])
                    ))
            
            # Competency assessments
            for comp in competencies:
                if random.random() > 0.3:
                    grade = random.choice([1, 2, 3, 3, 3, 4, 5])
                    grade_not_obs = 1 if random.random() > 0.85 else 0
                    
                    self.session.add(CompetencyAssessment(
                        session_id=session.session_id,
                        competency_id=comp.competency_id,
                        how_many=random.choice(["All", "Most", "Some", "Few"]),
                        how_often=random.choice(["Consistently", "Mostly consistent", "Inconsistently"]),
                        tem_outcome=random.choice(["Good safety margin", "Adequate margin", "Margin reduced"]),
                        grade=grade if grade_not_obs == 0 else None,
                        grade_not_observed=grade_not_obs,
                        evaluator_justification="Standard assessment"
                    ))
            
            self.session.commit()
            session_count += 1
            
            session_elapsed = time.perf_counter() - session_start
            print(f"  Session {session_count}: {session_elapsed:.3f}s")
        
        total_loop_elapsed = time.perf_counter() - session_loop_start
        log_time(f"{self.num_sessions} sessions loop", total_loop_elapsed)
        
        print(f"✓ Created {session_count} assessment sessions")

def generate_demo_data(num_sessions=5):
    generator = DemoDataGenerator(num_sessions=num_sessions)
    generator.generate_all()

if __name__ == "__main__":
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    generate_demo_data(num_sessions=num)
