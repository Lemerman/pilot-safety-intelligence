#!/usr/bin/env python
"""Generate demo data for testing and demonstration with timing and progress"""
import sys
import os
import time
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.base import SessionLocal
from models import (
    Pilot, PilotRole, Evaluator, EvaluatorType,
    Competency, CompetencyCode,
    AssessmentSession, AssessmentType, PhaseOfFlight, PFPMRole,
    Event,
    Threat, Error, UndesiredAircraftState, Countermeasure,
    CompetencyAssessment
)

class DemoDataGenerator:
    """Generate realistic demo data for testing and demonstration"""
    
    def __init__(self):
        self.session = SessionLocal()
        self.pilots = []
        self.evaluators = []
        self.competencies = []
        
    def generate_all(self):
        """Generate complete demo dataset"""
        start_time = time.time()
        try:
            print("\n" + "="*70)
            print("GENERATING DEMO DATA WITH TIMING")
            print("="*70)
            
            step_start = time.time()
            self.generate_pilots()
            print(f"  Elapsed: {time.time() - step_start:.2f}s")
            
            step_start = time.time()
            self.generate_evaluators()
            print(f"  Elapsed: {time.time() - step_start:.2f}s")
            
            step_start = time.time()
            self.generate_assessment_sessions()
            print(f"  Elapsed: {time.time() - step_start:.2f}s")
            
            total_elapsed = time.time() - start_time
            print("\n" + "="*70)
            print(f"✓ DEMO DATA GENERATION COMPLETE in {total_elapsed:.2f} seconds")
            print("="*70)
            
        except Exception as e:
            print(f"\n✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        finally:
            self.session.close()
    
    def generate_pilots(self):
        """Generate 20+ anonymous pilot records"""
        print("\nGenerating pilots...")
        roles = [PilotRole.CAPTAIN, PilotRole.FIRST_OFFICER]
        
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
        
        self.session.commit()
        print(f"✓ Created {len(self.pilots)} pilots")
    
    def generate_evaluators(self):
        """Generate 5 anonymous evaluator records"""
        print("Generating evaluators...")
        evaluator_types = [
            EvaluatorType.TRE,
            EvaluatorType.SIM,
            EvaluatorType.LTC,
            EvaluatorType.CHIEF,
            EvaluatorType.MANAGER
        ]
        
        evaluator_names = ["Evaluator A", "Evaluator B", "Evaluator C", "Evaluator D", "Evaluator E"]
        
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
        
        self.session.commit()
        print(f"✓ Created {len(self.evaluators)} evaluators")
    
    def generate_assessment_sessions(self):
        """Generate 100 realistic assessment sessions with full TEM data"""
        print("Generating assessment sessions...")
        
        # OPTIMIZATION: Cache all static lookups BEFORE loop
        competencies = self.session.query(Competency).all()
        print(f"  Loaded {len(competencies)} competencies from DB")
        
        assessment_types = list(AssessmentType)
        phases = list(PhaseOfFlight)
        pf_pm_roles = list(PFPMRole)
        comp_codes = [c.name for c in CompetencyCode]
        
        threat_types = ["Weather", "Aircraft Malfunction", "ATC Instruction", "Fatigue", "Runway Condition"]
        error_types = ["Procedural Error", "Communication Error", "Navigation Error", "Control Error", "Checklist Error"]
        uas_types = ["Altitude Deviation", "Speed Deviation", "Heading Deviation", "Descent Rate Deviation"]
        countermeasure_types = ["Technical", "Procedural", "CRM", "Automation"]
        
        threat_descriptions = [
            "Thunderstorm development in approach area",
            "Engine parameter fluctuation",
            "Hold instruction due to traffic",
            "Crew fatigue after long sector",
            "Wet runway conditions"
        ]
        
        error_descriptions = [
            "Forgot to extend flaps on time",
            "Missed radio callout",
            "Incorrect altitude set on descent",
            "Control input deviation from standard",
            "Incomplete pre-landing checklist"
        ]
        
        uas_descriptions = [
            "Altitude 200 feet above target",
            "Speed 5 knots above target",
            "Heading 3 degrees off course",
            "Descent rate 100 fpm above target"
        ]
        
        session_count = 0
        tem_elements_count = 0
        comp_assessment_count = 0
        
        for session_num in range(100):
            pilot = random.choice(self.pilots)
            evaluator = random.choice(self.evaluators)
            
            # Session date
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
            
            # Create events with TEM data
            for _ in range(random.randint(1, 3)):
                event = Event(
                    session_id=session.session_id,
                    event_description=random.choice(["Normal cruise", "Approach phase", "Emergency scenario", "System management"]),
                    phase_of_flight=random.choice(phases)
                )
                self.session.add(event)
                self.session.flush()
                
                # Add TEM elements
                if random.random() > 0.3:
                    threat = Threat(
                        event_id=event.event_id,
                        threat_description=random.choice(threat_descriptions),
                        threat_type=random.choice(threat_types)
                    )
                    self.session.add(threat)
                    tem_elements_count += 1
                
                if random.random() > 0.5:
                    error = Error(
                        event_id=event.event_id,
                        error_description=random.choice(error_descriptions),
                        error_type=random.choice(error_types)
                    )
                    self.session.add(error)
                    tem_elements_count += 1
                
                if random.random() > 0.6:
                    uas = UndesiredAircraftState(
                        event_id=event.event_id,
                        state_description=random.choice(uas_descriptions),
                        state_type=random.choice(uas_types)
                    )
                    self.session.add(uas)
                    tem_elements_count += 1
                
                # Add countermeasures
                if random.random() > 0.4:
                    countermeasure = Countermeasure(
                        event_id=event.event_id,
                        countermeasure_description="Effective crew coordination and problem solving",
                        countermeasure_type=random.choice(countermeasure_types),
                        competency_involved=random.choice(comp_codes),
                        effectiveness=random.choice(["Effective", "Partially Effective", "Ineffective"])
                    )
                    self.session.add(countermeasure)
                    tem_elements_count += 1
            
            # Create competency assessments - using cached competencies
            for comp in competencies:
                if random.random() > 0.3:
                    grade = random.choice([1, 2, 3, 3, 3, 4, 5])
                    grade_not_obs = 1 if random.random() > 0.85 else 0
                    
                    assessment = CompetencyAssessment(
                        session_id=session.session_id,
                        competency_id=comp.competency_id,
                        how_many=random.choice(["All", "Most", "Some", "Few"]),
                        how_often=random.choice(["Consistently", "Mostly consistent", "Inconsistently"]),
                        tem_outcome=random.choice(["Good safety margin", "Adequate margin", "Margin reduced"]),
                        grade=grade if grade_not_obs == 0 else None,
                        grade_not_observed=grade_not_obs,
                        evaluator_justification="Standard assessment during session"
                    )
                    self.session.add(assessment)
                    comp_assessment_count += 1
            
            self.session.commit()
            session_count += 1
            
            if session_count % 10 == 0:
                print(f"  ... {session_count} sessions created ({tem_elements_count} TEM elements, {comp_assessment_count} competency assessments)")
        
        print(f"✓ Created {session_count} assessment sessions")
        print(f"  - TEM elements: {tem_elements_count}")
        print(f"  - Competency assessments: {comp_assessment_count}")

def generate_demo_data():
    """Entry point for demo data generation"""
    generator = DemoDataGenerator()
    generator.generate_all()

if __name__ == "__main__":
    generate_demo_data()
