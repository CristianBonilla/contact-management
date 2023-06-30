from typing import List, Dict, Any
import asyncio
from constants.constants import *
from starlette.concurrency import run_in_threadpool
from repositories.clickup import ClickUp
from repositories.hubspot import Hubspot
from schemas.contact import ContactBase, HubspotContact

def hubspot_contacts_to_clickup(hubspot: Hubspot, clickup: ClickUp, data_list: List[Dict[str, Any]]):
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
    print(synced_tasks)
    print('Full synchronization')
    print('Updating contacts state in Hubspot...')
    updated_contacts = hubspot.update_contacts(update_contacts=contacts)
    print(updated_contacts)
    print('Updated contacts state')

async def run_contacts_sync(hubspot: Hubspot, clickup: ClickUp, data_list: List[Dict[str, Any]]):
    await run_in_threadpool(lambda : hubspot_contacts_to_clickup(hubspot, clickup, data_list))
