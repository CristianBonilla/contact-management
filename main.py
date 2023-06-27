from fastapi import FastAPI
from routes.contact import contact

app = FastAPI()
app.include_router(contact)
