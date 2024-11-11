import psycopg2 as pg
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

conn = None
#. TODO: Override connection info
db_password = os.getenv("DB_PASSWORD")
print(db_password)

db_connection_str = f"host=localhost user=postgres dbname=assignment3 password={db_password} port=5432"
print(db_connection_str)
try:
    conn = conn = pg.connect(db_connection_str)
except Exception as err:
    print("Cannot Create DB Connection", err)
