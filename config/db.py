from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

meta = MetaData()

url = URL.create(
    drivername='postgresql',
    host='db.g97.io',
    port=5432,
    username='developer',
    password='qS*7Pjs3v0kw',
    database='data_analyst'
)

engine = create_engine(url)

connection = engine.connect()

Session = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()
