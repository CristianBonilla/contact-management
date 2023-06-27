from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db import get_session
from schemas.api_call import ApiCall
from repositories.api_call import get_api_calls

api_call = APIRouter(prefix='/api_call')

@api_call.get('/', response_model=list[ApiCall])
def get_all(session: Session = Depends(get_session)):
    api_calls = get_api_calls(session)
    return api_calls
