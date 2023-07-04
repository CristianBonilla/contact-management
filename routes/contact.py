import json
import asyncio
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from hubspot.crm.contacts.exceptions import ApiException
from constants.constants import *
from config.db import get_session
from utils.http import get_request
from background_tasks.sync import run_contacts_sync
from repositories.hubspot import Hubspot
from repositories.clickup import Clickup
import repositories.contact as contact_repo
from models.sync import HubspotToClickup, ApiCallHubspotToClickup
from schemas.contact import ContactRequest

contact = APIRouter(prefix='/contact')

SessionDependency = Annotated[Session, Depends(get_session)]
HubspotDependency = Annotated[Hubspot, Depends(lambda : Hubspot(HUBSPOT_TOKEN))]
ClickupDependency = Annotated[Clickup, Depends(lambda : Clickup(CLICKUP_TOKEN, CLICKUP_LIST_ID))]

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
    contacts = hubspot.search_contacts_by_clickup_state()
    endpoint, params = await get_request(request, 'sync_contacts')
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
