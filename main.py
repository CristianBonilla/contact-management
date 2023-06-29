from fastapi import FastAPI
from config.db import engine, Base
from routes.api_call import api_call
from routes.contact import contact
from middlewares.api_call import ApiCallMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_call)
app.include_router(contact)

app.add_middleware(ApiCallMiddleware)
