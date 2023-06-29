from typing import List
import hubspot
from hubspot.crm.contacts import SimplePublicObjectInputForCreate, BatchInputSimplePublicObjectBatchInput, PublicObjectSearchRequest
from hubspot.crm.contacts.exceptions import ApiException
from hubspot.crm.properties import ModelProperty, PropertyCreate
from schemas.contact import ContactRequest, ClickUpState, UpdateHubspotContacts

client = hubspot.Client.create(access_token='pat-na1-bfa3f0c0-426b-4f0e-b514-89b20832c96a')

def add_contact(contact_request: ContactRequest, clickup_state = ClickUpState.NOT_SYNCHRONIZED):
    contact_object = SimplePublicObjectInputForCreate(
        properties={
            'email': contact_request.email,
            'firstname': contact_request.firstname,
            'lastname': contact_request.lastname,
            'phone': contact_request.phone,
            'website': contact_request.website,
            'clickup_state': clickup_state.value
        },
        associations=[]
    )
    try:
        contact = client.crm.contacts.basic_api.create(
            simple_public_object_input_for_create=contact_object
        )
        return {
            'id': contact.id,
            'properties': contact.properties,
            'properties_with_history': contact.properties_with_history,
            'archived': contact.archived,
            'archived_at': contact.archived_at
        }
    except ApiException as exception:
        raise exception

def update_contacts(update_contacts: List[UpdateHubspotContacts], clickup_state = ClickUpState.SYNCHRONIZED):
    update_contacts_object = BatchInputSimplePublicObjectBatchInput(
        inputs=list(map(
            lambda contact : {
                'id': contact.id,
                'properties': {
                    'email': contact.properties.email,
                    'firstname': contact.properties.firstname,
                    'lastname': contact.properties.lastname,
                    'phone': contact.properties.phone,
                    'website': contact.properties.website,
                    'clickup_state': clickup_state.value
                }
            }, update_contacts
        )))
    try:
        contacts = client.crm.contacts.batch_api.update(
            batch_input_simple_public_object_batch_input=update_contacts_object
        )
        return list(map(
            lambda contact : {
                'id': contact.id,
                'properties': contact.properties,
                'properties_with_history': contact.properties_with_history,
                'archived': contact.archived,
                'archived_at': contact.archived_at
            }, contacts.results
        ))
    except ApiException as expression:
        raise expression

def search_by_contacts_clickup_state(clickup_state = ClickUpState.NOT_SYNCHRONIZED, limit=100):
    contact_search = PublicObjectSearchRequest(
        filter_groups=[
            {
                'filters': [
                    {
                        'propertyName': 'clickup_state',
                        'value': clickup_state.value,
                        'operator': 'EQ'
                    }
                ]
            }
        ],
        properties=[
            'email',
            'firstname',
            'lastname',
            'phone',
            'website',
            'clickup_state'
        ],
        limit=limit)
    try:
        contacts = client.crm.contacts.search_api.do_search(
            public_object_search_request=contact_search
        )
        return list(map(
            lambda contact : {
                'id': contact.id,
                'properties': contact.properties,
                'properties_with_history': contact.properties_with_history,
                'archived': contact.archived,
                'archived_at': contact.archived_at
            }, contacts.results
        ))
    except ApiException as expression:
        raise expression

def load_clickup_state_property():
    clickup_state_property: ModelProperty
    try:
        clickup_state_property = client.crm.properties.core_api.get_by_name(
            object_type='contacts',
            property_name='clickup_state',
            archived=False
        )
        return clickup_state_property
    except ApiException as exception:
        if (exception.status == 404):
            clickup_state_property = create_clickup_state_property()
        raise exception

def create_clickup_state_property():
    property_object = PropertyCreate(
        name='clickup_state',
        label='ClickUp State',
        type='bool',
        field_type='booleancheckbox',
        group_name='contactinformation',
        options=[
            {
                'label': 'Synchronized',
                'description': 'The contact was synced in ClickUp',
                'value': True,
                'displayOrder': 1,
                'hidden': False
            },
            {
                'label': 'Not Synchronized',
                'description': 'The contact has not been synced in ClickUp',
                'value': False,
                'displayOrder': 2,
                'hidden': False
            }
        ],
        has_unique_value=False,
        hidden=False,
        form_field=True)
    try:
        clickup_state_property = client.crm.properties.core_api.create(
            object_type='contacts',
            property_create=property_object
        )
        return clickup_state_property
    except ApiException as exception:
        raise exception
