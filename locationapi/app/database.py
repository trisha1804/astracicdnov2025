import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
load_dotenv()

MYSQL_USER:str=os.getenv("MYSQL_USER")
MYSQL_PASSWORD:str=os.getenv("MYSQL_PASSWORD")
MYSQL_HOST:str=os.getenv("MYSQL_HOST")
MYSQL_PORT:int=os.getenv("MYSQL_PORT")
MYSQL_DB:str=os.getenv("MYSQL_DB")
print(f"MYSQL_USER: {MYSQL_USER}")
print(f"MYSQL_PASSWORD: {MYSQL_PASSWORD}")  
print(f"MYSQL_HOST: {MYSQL_HOST}")
print(f"MYSQL_PORT: {MYSQL_PORT}")
print(f"MYSQL_DB: {MYSQL_DB}")

#SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
#establishing the connection with mysql database
#mysql+pymysql://<username>:<password>@<host>/<dbname>
connection_url = URL.create(
    drivername="mysql+pymysql",
    username=MYSQL_USER,
    password=MYSQL_PASSWORD,  # raw password allowed
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DB,
)
engine = create_engine(
    connection_url,
    echo=True,          # set False in production
    future=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create a Base class for our models to inherit from declarative_base
# This Base class maintains a catalog of classes and tables relative to that base
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()