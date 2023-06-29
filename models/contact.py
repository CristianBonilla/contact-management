from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import Base

class Contact(Base):
    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False),
    website = Column(String(255), nullable=False)
