import json
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from hubspot.crm.contacts.exceptions import ApiException
from constants.constants import *
from config.db import get_session
from tasks.sync import run_contacts_sync
import repositories.api_call as api_call_repo
from repositories.clickup import ClickUp
from repositories.hubspot import Hubspot
import repositories.contact as contact_repo
from schemas.api_call import ApiCallRequest
from schemas.contact import ContactRequest

contact = APIRouter(prefix='/contact')

SessionDependency = Annotated[Session, Depends(get_session)]
HubspotDependency = Annotated[Hubspot, Depends(lambda : Hubspot(HUBSPOT_TOKEN))]
ClickupDependency = Annotated[ClickUp, Depends(lambda : ClickUp(CLICKUP_TOKEN, CLICKUP_LIST_ID))]

@contact.post('')
async def add_contact(contact_request: ContactRequest, hubspot: HubspotDependency, session: SessionDependency):
    endpoint = contact.url_path_for('add_contact')
    params = contact_request
    try:
        hubspot_contact = hubspot.add_contact(contact_request)
        contact_repo.add_contact(session, contact_request)
        api_call_repo.add_api_call(session, ApiCallRequest(
            endpoint=endpoint,
            params=params,
            result=json.dumps(hubspot_contact)
        ))
        return hubspot_contact
    except ApiException as exception:
        detail = { 'errors': [json.loads(exception.body)] }
        api_call_repo.add_api_call(session, ApiCallRequest(
            endpoint=endpoint,
            params=params,
            result=json.dumps({ 'detail': detail })
        ))
        raise HTTPException(
            status_code=exception.status,
            detail=detail
        )

@contact.post('/sync')
async def sync_contacts(request: Request, background_tasks: BackgroundTasks, hubspot: HubspotDependency, clickup: ClickupDependency, session: SessionDependency):
    endpoint = contact.url_path_for('sync_contacts')
    params = await request.json()
    contacts = hubspot.search_by_contacts_clickup_state()
    api_call_repo.add_api_call(session, ApiCallRequest(
        endpoint=endpoint,
        params=params,
        result=json.dumps(contacts)
    ))
    background_tasks.add_task(
        run_contacts_sync,
        endpoint,
        params,
        hubspot,
        clickup,
        session,
        contacts)
    content = {
        'total': len(contacts),
        'description': 'Following contacts will be synced in ClickUp with background tasks',
        'contacts': contacts
    }
    return JSONResponse(
        status_code=200,
        content=content
    )
