import psycopg2
import urllib.parse as urlparse

NEON_URL = "postgresql://neondb_owner:npg_FpezTLm5bX2Z@ep-noisy-leaf-a11kkcfa-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def get_connection():
    # Parse the connection string
    result = urlparse.urlparse(NEON_URL)
    
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    
    return psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname,
        port=port,
        sslmode="require"    # 🔥 Neon requires SSL
    )
