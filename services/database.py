from models.base import init_database, SessionLocal, Base, engine
from models.competency import Competency, ObservableBehavior, CompetencyCode
from services.config_loader import ConfigLoader

def init_db():
    """Initialize database and load competency data"""
    print("Initializing database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    # Load competencies from config
    session = SessionLocal()
    try:
        # Check if competencies already exist
        existing = session.query(Competency).count()
        if existing == 0:
            print("Loading competencies from configuration...")
            config = ConfigLoader.load_competencies()
            competencies_data = config.get('competencies', {})
            
            for code_str, data in competencies_data.items():
                # Create competency
                competency = Competency(
                    code=CompetencyCode[code_str],
                    name=data.get('name'),
                    description=data.get('description')
                )
                session.add(competency)
                session.flush()
                
                # Add observable behaviors
                behaviors = data.get('observable_behaviors', [])
                for behavior_desc in behaviors:
                    behavior = ObservableBehavior(
                        competency_id=competency.competency_id,
                        description=behavior_desc
                    )
                    session.add(behavior)
            
            session.commit()
            print(f"✓ Loaded {len(competencies_data)} competencies with observable behaviors")
        else:
            print(f"✓ Competencies already loaded ({existing} found)")
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
    print("\n✓ Database initialization complete")
