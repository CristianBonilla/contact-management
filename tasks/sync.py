import json
import asyncio
from typing import List, Dict, Any
from constants.constants import *
from starlette.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from repositories.clickup import ClickUp
from repositories.hubspot import Hubspot
import repositories.api_call as api_call_repo
from schemas.api_call import ApiCallRequest
from schemas.contact import ContactBase, HubspotContact

def hubspot_update_contacts(endpoint: str, params, hubspot: Hubspot, session: Session, contacts: List[HubspotContact]):
    print('Updating contacts state in Hubspot...')
    updated_contacts = hubspot.update_contacts(update_contacts=contacts)
    api_call_repo.add_api_call(session, ApiCallRequest(
        endpoint=endpoint,
        params=params,
        result=json.dumps(updated_contacts)
    ))
    print(updated_contacts)
    print('Updated contacts state')

def hubspot_contacts_to_clickup(endpoint: str, params, hubspot: Hubspot, clickup: ClickUp, session: Session, data_list: List[Dict[str, Any]]):
    if len(data_list) == 0:
        print('No contacts to sync')
        return
    print('Synchronizing contacts to ClickUp...')
    contacts = list(map(
        lambda contact : HubspotContact(
            id=contact['id'],
            properties=ContactBase(
                email=contact['properties']['email'],
                firstname=contact['properties']['firstname'],
                lastname=contact['properties']['lastname'],
                phone=contact['properties']['phone'],
                website=contact['properties']['website']
            )
       ), data_list
    ))
    synced_tasks = []
    asyncio.run(clickup.create_tasks(contacts, synced_tasks))
    api_call_repo.add_api_call(session, ApiCallRequest(
        endpoint=endpoint,
        params=params,
        result=json.dumps(synced_tasks)
    ))
    print(synced_tasks)
    print('Full synchronization')
    hubspot_update_contacts(endpoint, params, hubspot, session, contacts)

async def run_contacts_sync(endpoint: str, params, hubspot: Hubspot, clickup: ClickUp, session: Session, data_list: List[Dict[str, Any]]):
    await run_in_threadpool(lambda : hubspot_contacts_to_clickup(endpoint, params, hubspot, clickup, session, data_list))
