import json
import asyncio
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from hubspot.crm.contacts.exceptions import ApiException
from constants.constants import *
from config.db import get_session
from background_tasks.sync import run_contacts_sync
from repositories.hubspot import Hubspot
from repositories.clickup import ClickUp
import repositories.contact as contact_repo
from models.sync import HubspotToClickup, ApiCallHubspotToClickup
from schemas.contact import ContactRequest

contact = APIRouter(prefix='/contact')

SessionDependency = Annotated[Session, Depends(get_session)]
HubspotDependency = Annotated[Hubspot, Depends(lambda : Hubspot(HUBSPOT_TOKEN))]
ClickupDependency = Annotated[ClickUp, Depends(lambda : ClickUp(CLICKUP_TOKEN, CLICKUP_LIST_ID))]

@contact.post('')
async def add_contact(contact_request: ContactRequest, hubspot: HubspotDependency, session: SessionDependency):
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
async def sync_contacts(request: Request, hubspot: HubspotDependency, clickup: ClickupDependency, session: SessionDependency):
    endpoint = contact.url_path_for('sync_contacts')
    params = await request.json()
    contacts = hubspot.search_by_contacts_clickup_state()
    asyncio.create_task(run_contacts_sync(HubspotToClickup(
        session=session,
        hubspot=hubspot,
        clickup=clickup,
        api_call=ApiCallHubspotToClickup(
            endpoint=endpoint,
            params=params
        ),
        data=contacts
    )))
    return JSONResponse(
        status_code=200,
        content={
            'total': len(contacts),
            'description': 'Following contacts will be synced in ClickUp with background tasks',
            'contacts': contacts
        })
