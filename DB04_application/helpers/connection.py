import psycopg2 as pg

conn = None

# TODO: Override connection info

db_connection_str = "host=localhost user=postgres dbname=assignment3 password=0000 port=5432"

try:
    conn = conn = pg.connect(db_connection_str)
except Exception as err:
    print("Cannot Create DB Connection", err)
