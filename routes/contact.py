import json
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from hubspot.crm.contacts.exceptions import ApiException
from config.db import get_session
from repositories.clickup import ClickUp
import repositories.hubspot as hubspot_repo
import repositories.contact as contact_repo
from schemas.contact import ContactRequest

contact = APIRouter(prefix='/contact')

SessionDependency = Annotated[Session, Depends(get_session)]
ClickupDependency = Annotated[ClickUp, Depends(
    lambda : ClickUp(
        'pk_3182376_Q233NZDZ8AVULEGGCHLKG2HFXWD6MJLC',
        900200532843
    )
)]

@contact.post('')
def add_contact(contact_request: ContactRequest,  session: SessionDependency):
    try:
        hubspot_contact = hubspot_repo.add_contact(contact_request)
        contact_repo.add_contact(session, contact_request)
        return hubspot_contact
    except ApiException as exception:
        raise HTTPException(
            status_code=exception.status,
            detail={ 'errors': [json.loads(exception.body)] }
        )

@contact.post('/sync')
def sync_contacts(clickup: ClickupDependency):
    contacts = hubspot_repo.search_by_contacts_clickup_state()
    return contacts
