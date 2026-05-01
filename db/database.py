from config import Config
import sqlmodel as sqlm
import psycopg2 as sql

URI = str(Config.DATABASE_URI)

conn = sql.connect(Config.DATABASE_URI)

 
engine = sqlm.create_engine(URI, echo=True)
def create_engine():
    sqlm.SQLModel.metadata.create_all(engine)

session = sqlm.Session(engine)
