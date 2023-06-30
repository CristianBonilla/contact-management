from fastapi import FastAPI
from config.db import engine, Base
from routes.contact import contact

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(contact)
