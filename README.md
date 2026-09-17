# Pilot Safety Intelligence
# ICAO/IATA-aligned pilot competency assessment and safety intelligence platform

## Overview

This application provides a structured, evidence-based system for recording and analyzing pilot competency assessments aligned with:
- ICAO Competency-Based Training and Assessment (CBTA)
- ICAO Doc 9868 PANS-TRG
- Threat and Error Management (TEM)
- IATA Evidence-Based Training (EBT)
- ICAO ADREP / ECCAIRS safety taxonomy

## Key Features (Phase 1)

- SQLite database with SQLAlchemy ORM
- Configurable competency model (9 ICAO competencies)
- Observable behavior recording
- TEM (Threat, Error, Undesired State, Countermeasure, Recovery) data capture
- Safety occurrence taxonomy
- Demo data generator with 20+ pilots, 5 evaluators, 100+ assessments
- Basic test suite

## Installation

```bash
git clone https://github.com/Lemerman/pilot-safety-intelligence.git
cd pilot-safety-intelligence
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Initialization

```bash
# Initialize database
python scripts/init_db.py

# Generate demo data
python scripts/seed_demo_data.py

# Run tests
pytest tests/ -v
```

## Running the Application (Phase 2+)

```bash
streamlit run app.py
```

## Project Structure

```
pilot-safety-intelligence/
├── app.py                          # Main Streamlit application (Phase 2+)
├── requirements.txt                # Project dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
│
├── config/                         # Configuration files
│   ├── competencies.yaml           # 9 ICAO competencies and OBs
│   ├── grading.yaml                # Assessment scales and grade definitions
│   ├── taxonomy.yaml               # Safety occurrence taxonomy
│   └── __init__.py
│
├── models/                         # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── base.py                     # Base model class
│   ├── pilot.py                    # Pilot entity
│   ├── evaluator.py                # Evaluator/Instructor entity
│   ├── session.py                  # Assessment session
│   ├── competency.py               # Competency definitions
│   ├── observation.py              # Observable behaviors and observations
│   ├── tem.py                       # Threat, Error, UAS, Countermeasure
│   └── safety.py                   # Safety occurrence tracking
│
├── services/                       # Business logic
│   ├── __init__.py
│   ├── database.py                 # Database connection and initialization
│   ├── config_loader.py            # Load YAML configurations
│   └── demo_data.py                # Demo data generation
│
├── scripts/                        # Standalone scripts
│   ├── init_db.py                  # Initialize database schema
│   ├── seed_demo_data.py           # Generate demo data
│   └── __init__.py
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── test_database.py            # Database creation and integrity
│   ├── test_models.py              # ORM model tests
│   ├── test_demo_data.py           # Demo data generation tests
│   └── conftest.py                 # Pytest fixtures
│
├── data/                           # Runtime data folder
│   └── .gitkeep
│
└── analytics/                      # Analytics modules (Phase 4+)
    ├── __init__.py
    └── dashboard.py
```

## Assumptions for Phase 1

1. **Database**: SQLite stored locally in `data/` folder for simplicity
2. **Anonymization**: Pilots and evaluators assigned UUID identifiers; names not stored in core analytics tables
3. **Pilot Roles**: Captain, First Officer
4. **Aircraft**: A320 as baseline fleet
5. **Assessment Types**: Simulator, EBT, Line Check, Recurrent Training, Training Scenario
6. **Phases of Flight**: Pre-flight, Takeoff, Climb, Cruise, Descent, Approach, Landing, Post-flight
7. **Competencies**: 9 ICAO competencies as specified (KNO, PRO, COM, FPA, FPM, LTW, PSD, SAW, WLM)
8. **Grading Scale**: 1–5 with N/O (Not Observed) option; Grade 3 = adequate/expected
9. **TEM Structure**: Multiple threats/errors linked to single event; competencies as countermeasures
10. **Safety Taxonomy**: ICAO ADREP-style occurrence classification; supports import from CSV/JSON
11. **Demo Data**: 20 anonymous pilots, 5 evaluators, 100 assessment sessions, realistic variation
12. **No Regulatory Approval**: System is decision-support only; grading descriptions stored in config files

## Regulatory Framework & Disclaimer

This platform is designed as a **decision-support and training intelligence system** aligned with:
- ICAO Competency-Based Training and Assessment principles
- IATA Evidence-Based Training methodology
- Threat and Error Management concepts

**It does NOT provide regulatory certification or approval.**

All grading descriptions, competency definitions, and assessment criteria must be validated by the operator and aligned with:
- National aviation authority requirements
- Operator's Training and Qualification Manual (TQM)
- CAMO/AOC-specific procedures

Individual assessment results must not be interpreted as a unilateral determination of pilot fitness without human review and organizational context.

## Phase 1 Deliverables

✅ SQLite database with 8 core tables  
✅ SQLAlchemy ORM models and relationships  
✅ YAML configuration files for competencies, grading, taxonomy  
✅ Database initialization script  
✅ Realistic demo-data generator (20 pilots, 5 evaluators, 100+ sessions)  
✅ TEM data structures and relationships  
✅ Observable behavior and competency assessment structures  
✅ Basic automated test suite  

## Next Phases

- Phase 2: New Assessment workflow (Streamlit UI)
- Phase 3: Pilot Competency Profile
- Phase 4: Dashboard & Analytics
- Phase 5: TEM / Safety Analysis
- Phase 6: Instructor Concordance
- Phase 7: Data Export (CSV, Excel, PDF)

## Development Notes

- All timestamps are UTC
- Pilot IDs and Evaluator IDs are UUIDs (anonymized)
- Session IDs are also UUIDs for traceability
- Observable Behavior classification is evidence-based (Observe → Record → Classify → Assess)
- Competency assessment uses: HOW MANY, HOW OFTEN, TEM OUTCOME dimensions
- No AI-generated scores; all assessments require human evaluator input
- Grading descriptions and competency definitions are configurable and organization-specific

## Support & Questions

See the application's "Source/Methodology" page (Phase 2+) for regulatory framework details and assessment methodology.

---

**Status**: Phase 1 (Database & Data) - WORKING  
**Last Updated**: 2026-09-17  
**Maintainer**: Aviation Safety Intelligence Community
