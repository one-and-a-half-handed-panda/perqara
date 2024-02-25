import sqlalchemy.engine.url
from env_variables import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USERNAME
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DB_URL = sqlalchemy.engine.url.URL.create(
    drivername='postgresql+psycopg2',
    username=DB_USERNAME,
    password=DB_PASSWORD,
    database=DB_NAME,
    host=DB_HOST,
    port=DB_PORT,
)

db_engine = create_engine(DB_URL)

def get_db_session() -> Session:
    with Session(db_engine) as db:
        yield db