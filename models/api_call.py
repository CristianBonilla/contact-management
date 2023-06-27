from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Integer, TIMESTAMP, String, JSON, TEXT
from config.db import Base

class ApiCall(Base):
    __tablename__ = 'api_calls'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    endpoint = Column(String(255), nullable=False, index=True)
    params = Column(JSON)
    result = Column(TEXT)
