#!/usr/bin/env python
"""Phase 1 Completion Verification - Initialize DB, Generate Demo Data, Validate"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.base import Base, engine, SessionLocal
from services.database import init_db
from services.demo_data import generate_demo_data
from models import (
    Pilot, Evaluator, Competency, AssessmentSession, Event,
    Threat, Error, UndesiredAircraftState, Countermeasure,
    CompetencyAssessment, Observation, SafetyOccurrence
)

print("\n" + "="*70)
print("PHASE 1 COMPLETION VERIFICATION")
print("="*70)

print("\n[STEP 1] Initializing database...")
try:
    init_db()
    print("✓ Database initialized successfully")
except Exception as e:
    print(f"✗ Database initialization failed: {e}")
    sys.exit(1)

print("\n[STEP 2] Generating demo data...")
try:
    generate_demo_data()
    print("✓ Demo data generated successfully")
except Exception as e:
    print(f"✗ Demo data generation failed: {e}")
    sys.exit(1)

print("\n[STEP 3] Verifying database records...")
session = SessionLocal()
try:
    pilot_count = session.query(Pilot).count()
    evaluator_count = session.query(Evaluator).count()
    competency_count = session.query(Competency).count()
    assessment_count = session.query(AssessmentSession).count()
    event_count = session.query(Event).count()
    threat_count = session.query(Threat).count()
    error_count = session.query(Error).count()
    uas_count = session.query(UndesiredAircraftState).count()
    countermeasure_count = session.query(Countermeasure).count()
    comp_assessment_count = session.query(CompetencyAssessment).count()
    observation_count = session.query(Observation).count()
    safety_occurrence_count = session.query(SafetyOccurrence).count()
    
    print(f"\nDatabase Record Counts:")
    print(f"  Pilots:                      {pilot_count}")
    print(f"  Evaluators:                  {evaluator_count}")
    print(f"  Competencies:                {competency_count}")
    print(f"  Assessment Sessions:         {assessment_count}")
    print(f"  Events:                      {event_count}")
    print(f"  Threats:                     {threat_count}")
    print(f"  Errors:                      {error_count}")
    print(f"  Undesired Aircraft States:   {uas_count}")
    print(f"  Countermeasures:             {countermeasure_count}")
    print(f"  Competency Assessments:      {comp_assessment_count}")
    print(f"  Observations:                {observation_count}")
    print(f"  Safety Occurrences:          {safety_occurrence_count}")
    
    # Validation checks
    print(f"\nValidation Checks:")
    checks_passed = 0
    checks_total = 6
    
    if pilot_count >= 20:
        print(f"  ✓ Pilots: {pilot_count} >= 20")
        checks_passed += 1
    else:
        print(f"  ✗ Pilots: {pilot_count} < 20")
    
    if evaluator_count >= 5:
        print(f"  ✓ Evaluators: {evaluator_count} >= 5")
        checks_passed += 1
    else:
        print(f"  ✗ Evaluators: {evaluator_count} < 5")
    
    if competency_count == 9:
        print(f"  ✓ Competencies: {competency_count} == 9")
        checks_passed += 1
    else:
        print(f"  ✗ Competencies: {competency_count} != 9")
    
    if assessment_count >= 100:
        print(f"  ✓ Assessment Sessions: {assessment_count} >= 100")
        checks_passed += 1
    else:
        print(f"  ✗ Assessment Sessions: {assessment_count} < 100")
    
    if event_count > 0:
        print(f"  ✓ Events: {event_count} > 0")
        checks_passed += 1
    else:
        print(f"  ✗ Events: {event_count} == 0")
    
    if comp_assessment_count > 0:
        print(f"  ✓ Competency Assessments: {comp_assessment_count} > 0")
        checks_passed += 1
    else:
        print(f"  ✗ Competency Assessments: {comp_assessment_count} == 0")
    
    print(f"\nValidation Result: {checks_passed}/{checks_total} checks passed")
    
    if checks_passed == checks_total:
        print("\n" + "="*70)
        print("✓ PHASE 1 VALIDATION PASSED")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("✗ PHASE 1 VALIDATION INCOMPLETE")
        print("="*70)
        sys.exit(1)

finally:
    session.close()
