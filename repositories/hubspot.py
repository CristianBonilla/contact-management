from typing import List
import hubspot
from hubspot.crm.contacts import SimplePublicObject, SimplePublicObjectInputForCreate, BatchResponseSimplePublicObject, BatchInputSimplePublicObjectBatchInput, PublicObjectSearchRequest, CollectionResponseWithTotalSimplePublicObjectForwardPaging
from hubspot.crm.contacts.exceptions import ApiException
from hubspot.crm.properties import ModelProperty, PropertyCreate
from models.hubspot import HubspotContact, ClickUpState
from schemas.contact import ContactRequest

class Hubspot:
    def __init__(self, token: str):
        self.client = hubspot.Client.create(access_token=token)
        self.load_clickup_state_property()

    def add_contact(self, contact_request: ContactRequest, clickup_state = ClickUpState.NOT_SYNCED):
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
            contact: SimplePublicObject = self.client.crm.contacts.basic_api.create(
                simple_public_object_input_for_create=contact_object
            )
            return {
                'id': contact.id,
                'created_at': contact.created_at.isoformat(),
                'updated_at': contact.updated_at.isoformat(),
                'properties': contact.properties,
                'properties_with_history': contact.properties_with_history,
                'archived': contact.archived,
                'archived_at': contact.archived_at
            }
        except ApiException as exception:
            raise exception

    def update_contacts(self, update_contacts: List[HubspotContact], clickup_state = ClickUpState.SYNCED):
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
            updated_contacts: BatchResponseSimplePublicObject = self.client.crm.contacts.batch_api.update(
                batch_input_simple_public_object_batch_input=update_contacts_object
            )
            contacts: List[SimplePublicObject] = updated_contacts.results
            return list(map(
                lambda contact : {
                    'id': contact.id,
                    'created_at': contact.created_at.isoformat(),
                    'updated_at': contact.updated_at.isoformat(),
                    'properties': contact.properties,
                    'properties_with_history': contact.properties_with_history,
                    'archived': contact.archived,
                    'archived_at': contact.archived_at
                }, contacts
            ))
        except ApiException as expression:
            raise expression

<<<<<<< Updated upstream
    def search_by_contacts_clickup_state(self, clickup_state = ClickUpState.NOT_SYNCED, limit=100):
=======
    def search_contacts_by_clickup_state(self, clickup_state = ClickupState.NOT_SYNCED, limit=100):
>>>>>>> Stashed changes
        clickup_state_value = str(clickup_state.value).lower()
        contacts_search_object = PublicObjectSearchRequest(
            filter_groups=[
                {
                    'filters': [
                        {
                            'propertyName': 'clickup_state',
                            'operator': 'HAS_PROPERTY'
                        },
                        {
                            'propertyName': 'clickup_state',
                            'value': clickup_state_value,
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
            contacts_found: CollectionResponseWithTotalSimplePublicObjectForwardPaging = self.client.crm.contacts.search_api.do_search(
                public_object_search_request=contacts_search_object
            )
            contacts: List[SimplePublicObject] = list(filter(lambda contact : contact.properties['clickup_state'] == clickup_state_value, contacts_found.results))
            return list(map(
                lambda contact : {
                    'id': contact.id,
                    'created_at': contact.created_at.isoformat(),
                    'updated_at': contact.updated_at.isoformat(),
                    'properties': contact.properties,
                    'properties_with_history': contact.properties_with_history,
                    'archived': contact.archived,
                    'archived_at': contact.archived_at
                }, contacts
            ))
        except ApiException as expression:
            raise expression

    def load_clickup_state_property(self):
        clickup_state_property: ModelProperty
        try:
            clickup_state_property = self.client.crm.properties.core_api.get_by_name(
                object_type='contacts',
                property_name='clickup_state',
                archived=False
            )
            return clickup_state_property
        except ApiException as exception:
            if (exception.status == 404):
                clickup_state_property = self.create_clickup_state_property()
            raise exception

    def create_clickup_state_property(self):
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
            clickup_state_property = self.client.crm.properties.core_api.create(
                object_type='contacts',
                property_create=property_object
            )
            return clickup_state_property
        except ApiException as exception:
            raise exception
