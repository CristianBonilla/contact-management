import json
from fastapi import APIRouter, HTTPException
from hubspot.crm.contacts.exceptions import ApiException
import repositories.hubspot as hubspot_repo
from schemas.contact import ContactRequest

contact = APIRouter(prefix='/contact')

@contact.post('')
def add_contact(contact_request: ContactRequest):
    try:
        hubspot_repo.load_clickup_state_property()
        return hubspot_repo.add_contact(contact_request)
    except ApiException as exception:
        raise HTTPException(
            status_code=exception.status,
            detail={ 'errors': [json.loads(exception.body)] }
        )

@contact.post('/synchronized')
def sync_contacts():
    return
