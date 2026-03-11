import os
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.database import SessionLocal, Base
from backend.models.activity import Activity, ImportRecord

def run_migration(pg_url: str, drop_existing: bool = False):
    """
    Migrates all data from the local SQLite database to a given PostgreSQL database.
    Format example: postgresql://user:password@localhost:5432/nexus_sports
    """
    print("Starting migration to PostgreSQL...")
    print(f"Target URL: {pg_url}")
    
    # Setup PG Engine
    try:
        pg_engine = create_engine(pg_url)
        PgSession = sessionmaker(autocommit=False, autoflush=False, bind=pg_engine)
        
        # Test connection
        pg_engine.connect().close()
        print("Connected to PostgreSQL successfully.")
    except Exception as e:
        print(f"Failed to connect to PostgreSQL: {e}")
        return

    # Create tables
    if drop_existing:
        print("Dropping existing tables in PG...")
        Base.metadata.drop_all(bind=pg_engine)
        
    print("Creating schema in PG...")
    Base.metadata.create_all(bind=pg_engine)
    
    # Read from SQLite
    print("Reading data from local SQLite database...")
    sqlite_db = SessionLocal()
    
    try:
        activities = sqlite_db.query(Activity).all()
        records = sqlite_db.query(ImportRecord).all()
        print(f"Found {len(activities)} activities and {len(records)} import records.")
    except Exception as e:
        print(f"Failed to read from local SQLite: {e}")
        sqlite_db.close()
        return
        
    # Write to PostgreSQL
    print("Migrating records...")
    pg_db = PgSession()
    
    try:
        # Migrate ImportRecords
        rc_count = 0
        for r in records:
            # Check if exists
            exists = pg_db.query(ImportRecord).filter(ImportRecord.file_hash == r.file_hash).first()
            if not exists:
                new_r = ImportRecord(**{c.name: getattr(r, c.name) for c in ImportRecord.__table__.columns if c.name != 'id'})
                # We can keep original ID if needed, but safer to let PG auto-increment
                new_r.id = r.id 
                pg_db.add(new_r)
                rc_count += 1
                
        # Migrate Activities
        ac_count = 0
        for a in activities:
            exists = pg_db.query(Activity).filter(Activity.original_file_hash == a.original_file_hash).first()
            if not exists:
                new_a = Activity(**{c.name: getattr(a, c.name) for c in Activity.__table__.columns if c.name != 'id'})
                new_a.id = a.id
                pg_db.add(new_a)
                ac_count += 1
                
        pg_db.commit()
        print(f"Migration completed successfully!")
        print(f"Inserted: {ac_count} Activities, {rc_count} Import Records.")
        
    except Exception as e:
        pg_db.rollback()
        print(f"Error during migration, transaction rolled back. Error: {e}")
    finally:
        pg_db.close()
        sqlite_db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migration utility from SQLite to PostgreSQL")
    parser.add_argument("pg_url", type=str, help="PostgreSQL connection string")
    parser.add_argument("--drop", action="store_true", help="Drop existing tables in target database before migrating")
    
    args = parser.parse_args()
    run_migration(args.pg_url, drop_existing=args.drop)
