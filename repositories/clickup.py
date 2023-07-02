import json
import aiohttp
import asyncio
from typing import List
from time import time
from models.hubspot import HubspotContact

class ClickUp:
    def __init__(self, token: str, list_id: int):
        self.token = token
        self.list_id = list_id

    async def create_tasks(self, hubspot_contacts: List[HubspotContact], synced_tasks: List):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for contact in hubspot_contacts:
                tasks.append(asyncio.ensure_future(self._create_task(session, contact)))
            synced_tasks.extend(await asyncio.gather(*tasks))
            for task in synced_tasks:
                return task

    async def _create_task(self, session: aiohttp.ClientSession, hubspot_contact: HubspotContact):
        contact_id = hubspot_contact.id
        contact = hubspot_contact.properties
        try:
            url = 'https://api.clickup.com/api/v2/list/%s/task' % self.list_id
            headers = {
                'Content-Type': 'application/json',
                'Authorization': self.token
            }
            payload = {
                'name': 'Contact #%s: %s %s' % (contact_id, contact.firstname, contact.lastname),
                'description': 'Creating a contact task from hubspot %s %s %s' % (contact.phone, contact.email, contact.website),
                'assignees': [],
                'tags': [],
                'priority': 3,
                'due_date': None,
                'due_date_time': False,
                'time_estimate': None,
                'start_date': int(time()),
                'start_date_time': True,
                'notify_all': True,
                'parent': None,
                'links_to': None,
                'check_required_custom_fields': True,
                'custom_fields': []
            }
            async with session.post(url, json=payload, headers=headers) as task_response:
                task = await task_response.read()
                hashrate = json.loads(task)
                return hashrate
        except Exception as exception:
            raise exception
