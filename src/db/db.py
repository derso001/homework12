from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE = {
    'ENGINE': 'postgresql+psycopg2',
    'NAME': 'postgres',
    'USER': 'postgres',
    'PASSWORD': '1111',
    'HOST': '127.0.0.1',
    'PORT': '5432',
}

CONNECTION_STRING = f"{DATABASE['ENGINE']}://{DATABASE['USER']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['NAME']}"

engine = create_engine(CONNECTION_STRING)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)