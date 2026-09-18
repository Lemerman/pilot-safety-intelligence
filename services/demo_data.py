import random
import threading
import time
from datetime import UTC, datetime, timedelta
from sqlalchemy import delete
from models.base import SessionLocal
from models import (
    Pilot, PilotRole, Evaluator, EvaluatorType,
    Competency, CompetencyCode, ObservableBehavior,
    AssessmentSession, AssessmentType, PhaseOfFlight, PFPMRole,
    Event, Observation, ObservationType,
    Threat, Error, UndesiredAircraftState, Countermeasure,
    CompetencyAssessment, PilotCompetencyProfile
)


_STATUS = {
    "current_step": "idle",
    "session_count": 0,
    "last_progress_monotonic": time.monotonic(),
}
_STATUS_LOCK = threading.Lock()


def _log(message):
    print(f"{datetime.now(UTC).isoformat(timespec='seconds').replace('+00:00', 'Z')} {message}", flush=True)


def _update_status(step, session_count=None):
    with _STATUS_LOCK:
        _STATUS["current_step"] = step
        if session_count is not None:
            _STATUS["session_count"] = session_count
        _STATUS["last_progress_monotonic"] = time.monotonic()


def get_demo_data_status():
    with _STATUS_LOCK:
        return dict(_STATUS)


class DemoDataGenerator:
    """Generate realistic demo data for testing and demonstration"""
    
    def __init__(self):
        self.session = SessionLocal()
        self.pilots = []
        self.evaluators = []
        self.competencies = []
        
    def generate_all(self):
        """Generate complete demo dataset"""
        try:
            overall_start = time.perf_counter()
            _update_status("starting")
            _log("=" * 60)
            _log("GENERATING DEMO DATA")
            _log("=" * 60)

            self._run_timed_step("ensure_reference_data", self.ensure_reference_data)
            self.reset_demo_data()
            self._run_timed_step("generate_pilots", self.generate_pilots)
            self._run_timed_step("generate_evaluators", self.generate_evaluators)
            self._run_timed_step("generate_assessment_sessions", self.generate_assessment_sessions)

            elapsed = time.perf_counter() - overall_start
            _update_status("complete", self.session.query(AssessmentSession).count())
            _log("=" * 60)
            _log(f"DEMO DATA GENERATION COMPLETE in {elapsed:.3f}s")
            _log("=" * 60)
        except Exception:
            status = get_demo_data_status()
            _update_status("failed", status["session_count"])
            raise
        finally:
            self.session.close()

    def _run_timed_step(self, name, func):
        status = get_demo_data_status()
        _update_status(name, status["session_count"])
        _log(f"step={name} started session_count={status['session_count']}")
        step_start = time.perf_counter()
        func()
        elapsed = time.perf_counter() - step_start
        status = get_demo_data_status()
        _log(f"step={name} finished duration={elapsed:.3f}s session_count={status['session_count']}")

    def _timed_query_all(self, query, name):
        start = time.perf_counter()
        result = query.all()
        elapsed = time.perf_counter() - start
        status = get_demo_data_status()
        _log(f"query={name} duration={elapsed:.6f}s rows={len(result)} session_count={status['session_count']}")
        return result

    def ensure_reference_data(self):
        count_start = time.perf_counter()
        competency_count = self.session.query(Competency).count()
        count_elapsed = time.perf_counter() - count_start
        _log(
            f"query=competency_reference_data duration={count_elapsed:.6f}s "
            f"rows={competency_count} session_count={get_demo_data_status()['session_count']}"
        )
        if competency_count == 0:
            raise RuntimeError("No competencies loaded. Run scripts/init_db.py before scripts/seed_demo_data.py.")

    def reset_demo_data(self):
        _update_status("reset_demo_data")
        _log("step=reset_demo_data started session_count=0")
        start = time.perf_counter()
        for model in [
            PilotCompetencyProfile,
            CompetencyAssessment,
            Observation,
            Countermeasure,
            UndesiredAircraftState,
            Error,
            Threat,
            Event,
            AssessmentSession,
            Evaluator,
            Pilot,
        ]:
            delete_start = time.perf_counter()
            result = self.session.execute(delete(model))
            delete_elapsed = time.perf_counter() - delete_start
            _log(
                f"reset_table={model.__tablename__} deleted={result.rowcount} "
                f"delete_duration={delete_elapsed:.6f}s "
                f"session_count=0"
            )
        commit_start = time.perf_counter()
        self.session.commit()
        commit_elapsed = time.perf_counter() - commit_start
        elapsed = time.perf_counter() - start
        _log(f"step=reset_demo_data finished duration={elapsed:.3f}s commit_duration={commit_elapsed:.6f}s session_count=0")
    
    def generate_pilots(self):
        """Generate 20+ anonymous pilot records"""
        _update_status("generate_pilots")
        _log("Generating pilots...")
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

        commit_start = time.perf_counter()
        self.session.commit()
        commit_elapsed = time.perf_counter() - commit_start
        _log(
            f"✓ Created {len(self.pilots)} pilots commit_duration={commit_elapsed:.6f}s "
            f"session_count={get_demo_data_status()['session_count']}"
        )
    
    def generate_evaluators(self):
        """Generate 5 anonymous evaluator records"""
        _update_status("generate_evaluators")
        _log("Generating evaluators...")
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

        commit_start = time.perf_counter()
        self.session.commit()
        commit_elapsed = time.perf_counter() - commit_start
        _log(
            f"✓ Created {len(self.evaluators)} evaluators commit_duration={commit_elapsed:.6f}s "
            f"session_count={get_demo_data_status()['session_count']}"
        )
    
    def generate_assessment_sessions(self):
        """Generate 100+ realistic assessment sessions with full TEM data"""
        _update_status("generate_assessment_sessions", 0)
        _log("Generating assessment sessions...")
        
        assessment_types = list(AssessmentType)
        phases = list(PhaseOfFlight)
        pf_pm_roles = list(PFPMRole)
        
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

        competencies = self._timed_query_all(
            self.session.query(Competency),
            "competencies_for_assessments",
        )

        session_count = 0
        for _ in range(100):
            _update_status("generate_assessment_sessions.loop", session_count)
            pilot = random.choice(self.pilots)
            evaluator = random.choice(self.evaluators)
            
            # Session date
            days_ago = random.randint(1, 90)
            session_date = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=days_ago)
            
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
                
                if random.random() > 0.5:
                    error = Error(
                        event_id=event.event_id,
                        error_description=random.choice(error_descriptions),
                        error_type=random.choice(error_types)
                    )
                    self.session.add(error)
                
                if random.random() > 0.6:
                    uas = UndesiredAircraftState(
                        event_id=event.event_id,
                        state_description=random.choice(uas_descriptions),
                        state_type=random.choice(uas_types)
                    )
                    self.session.add(uas)
                
                # Add countermeasures (competency-linked)
                if random.random() > 0.4:
                    comp_codes = [c.name for c in CompetencyCode]
                    countermeasure = Countermeasure(
                        event_id=event.event_id,
                        countermeasure_description="Effective crew coordination and problem solving",
                        countermeasure_type=random.choice(countermeasure_types),
                        competency_involved=random.choice(comp_codes),
                        effectiveness=random.choice(["Effective", "Partially Effective", "Ineffective"])
                    )
                    self.session.add(countermeasure)
            
            # Create competency assessments
            for comp in competencies:
                if random.random() > 0.3:  # Not all competencies assessed in every session
                    grade = random.choice([1, 2, 3, 3, 3, 4, 5])  # Grade 3 is most common
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
            
            commit_start = time.perf_counter()
            self.session.commit()
            commit_elapsed = time.perf_counter() - commit_start
            session_count += 1
            _update_status("generate_assessment_sessions.committed", session_count)

            if session_count % 10 == 0:
                _log(
                    f"checkpoint session_count={session_count} "
                    f"last_commit_duration={commit_elapsed:.6f}s"
                )

        _log(f"✓ Created {session_count} assessment sessions with TEM data")

def generate_demo_data():
    """Entry point for demo data generation"""
    generator = DemoDataGenerator()
    generator.generate_all()

if __name__ == "__main__":
    generate_demo_data()
