from sqlalchemy.orm import Session
from models.api_call import ApiCall
from schemas.api_call import ApiCallRequest

def add_api_call(session: Session, api_call_request: ApiCallRequest):
    api_call = ApiCall(
        endpoint=api_call_request.endpoint,
        params=api_call_request.params,
        result=api_call_request.result
    )
    session.add(api_call)
    session.commit()
    session.refresh(api_call)
    return api_call

def get_api_call(session: Session, api_call_id: int):
    return session.query(ApiCall).filter(ApiCall.id == api_call_id).first()

def get_api_calls(session: Session, limit: int = 100):
    return session.query(ApiCall).limit(limit).all()
