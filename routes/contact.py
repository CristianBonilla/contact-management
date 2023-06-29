import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from hubspot.crm.contacts.exceptions import ApiException
from config.db import get_session
import repositories.hubspot as hubspot_repo
import repositories.contact as contact_repo
from schemas.contact import ContactRequest

contact = APIRouter(prefix='/contact')

@contact.post('')
def add_contact(contact_request: ContactRequest, session: Session = Depends(get_session)):
    try:
        hubspot_repo.load_clickup_state_property()
        hubspot_contact = hubspot_repo.add_contact(contact_request)
        contact_repo.add_contact(session, contact_request)
        return hubspot_contact
    except ApiException as exception:
        raise HTTPException(
            status_code=exception.status,
            detail={ 'errors': [json.loads(exception.body)] }
        )

@contact.post('/sync')
def sync_contacts():
    return
