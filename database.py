import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="fastapi",
        user="postgres",
        password=83100,
        host="localhost",
        port="5432"
    )