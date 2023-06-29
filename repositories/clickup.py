import sys
import requests
from time import time
from schemas.contact import ContactBase

class ClickUp:
    def __init__(self, token: str, list_id: int):
        self.token = token
        self.list_id = list_id

    def create_task(self, contact: ContactBase):
        try:
            url = 'https://api.clickup.com/api/v2/list/%s/task' % self.list_id
            headers = {
                'Content-Type': 'application/json',
                'Authorization': self.token
            }
            payload = {
                'name': 'Contact: %s %s' % (contact.firstname, contact.lastname),
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
            task_response = requests.post(url=url, headers=headers, json=payload)
            task = task_response.json()
            return task
        except:
            raise Exception(sys.exc_info())
