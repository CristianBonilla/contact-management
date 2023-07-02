import json
import asyncio
import repositories.api_call as api_call_repo
from models.sync import HubspotToClickup
from schemas.api_call import ApiCallRequest

def update_hubspot_contacts(hubspot_to_clickup: HubspotToClickup):
    print('Updating contacts state in Hubspot...')
    updated_contacts = hubspot_to_clickup.hubspot.update_contacts(update_contacts=hubspot_to_clickup.contacts)
    api_call_repo.add_api_call(hubspot_to_clickup.session, ApiCallRequest(
        endpoint=hubspot_to_clickup.api_call.endpoint,
        params=hubspot_to_clickup.api_call.params,
        result=json.dumps(updated_contacts)
    ))
    print(updated_contacts)
    print('Updated contacts state')

def hubspot_contacts_to_clickup(hubspot_to_clickup: HubspotToClickup):
    if len(hubspot_to_clickup.data) == 0:
        print('No contacts to sync')
        return
    print('Synchronizing contacts to ClickUp...')
    synced_tasks = []
    asyncio.run(hubspot_to_clickup.clickup.create_tasks(hubspot_to_clickup.contacts, synced_tasks))
    api_call_repo.add_api_call(hubspot_to_clickup.session, ApiCallRequest(
        endpoint=hubspot_to_clickup.api_call.endpoint,
        params=hubspot_to_clickup.api_call.params,
        result=json.dumps(synced_tasks)
    ))
    print(synced_tasks)
    print('Full synchronization')
    update_hubspot_contacts(hubspot_to_clickup)

async def run_contacts_sync(hubspot_to_clickup: HubspotToClickup):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, lambda : hubspot_contacts_to_clickup(hubspot_to_clickup))
