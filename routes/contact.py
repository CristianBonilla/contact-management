import json
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from hubspot.crm.contacts.exceptions import ApiException
from constants.constants import *
from config.db import get_session
from tasks.sync import run_contacts_sync
from repositories.clickup import ClickUp
from repositories.hubspot import Hubspot
import repositories.contact as contact_repo
from schemas.contact import ContactRequest

contact = APIRouter(prefix='/contact')

SessionDependency = Annotated[Session, Depends(get_session)]
HubspotDependency = Annotated[Hubspot, Depends(lambda : Hubspot(HUBSPOT_TOKEN))]
ClickupDependency = Annotated[ClickUp, Depends(lambda : ClickUp(CLICKUP_TOKEN, CLICKUP_LIST_ID))]

@contact.post('')
async def add_contact(contact_request: ContactRequest, hubspot: HubspotDependency,  session: SessionDependency):
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
async def sync_contacts(background_tasks: BackgroundTasks, hubspot: HubspotDependency, clickup: ClickupDependency):
    contacts = hubspot.search_by_contacts_clickup_state()
    background_tasks.add_task(run_contacts_sync, hubspot, clickup, contacts)
    return JSONResponse(
        status_code=200,
        content={
            'total': len(contacts),
            'description': 'Following contacts will be synced in ClickUp with background tasks',
            'contacts': contacts
        }
    )
