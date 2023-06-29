import json
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from hubspot.crm.contacts.exceptions import ApiException
from config.db import get_session
from repositories.clickup import ClickUp
from repositories.hubspot import Hubspot
import repositories.contact as contact_repo
from schemas.contact import ContactRequest

contact = APIRouter(prefix='/contact')

SessionDependency = Annotated[Session, Depends(get_session)]
HubspotDependency = Annotated[Hubspot, Depends(
    lambda : Hubspot('pat-na1-bfa3f0c0-426b-4f0e-b514-89b20832c96a')
)]
ClickupDependency = Annotated[ClickUp, Depends(
    lambda : ClickUp(
        'pk_3182376_Q233NZDZ8AVULEGGCHLKG2HFXWD6MJLC',
        900200532843
    )
)]

@contact.post('')
def add_contact(contact_request: ContactRequest, hubspot: HubspotDependency,  session: SessionDependency):
    try:
        hubspot_contact = hubspot.add_contact(contact_request)
        contact_repo.add_contact(session, contact_request)
        return hubspot_contact
    except ApiException as exception:
        raise HTTPException(
            status_code=exception.status,
            detail={ 'errors': [json.loads(exception.body)] }
        )

@contact.post('/sync')
def sync_contacts(hubspot: HubspotDependency, clickup: ClickupDependency):
    contacts = hubspot.search_by_contacts_clickup_state()
    return contacts
