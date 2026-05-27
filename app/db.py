import os

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

def get_db_connection():
    if not HAS_PSYCOPG2:
        print("psycopg2 not installed")
        return None
        
    try:
        conn = psycopg2.connect(
            os.environ.get('DATABASE_URL', 'postgresql://localhost/cc_benefit_tracker'),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
