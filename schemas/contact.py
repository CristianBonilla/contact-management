from enum import Enum
from pydantic import BaseModel

class ClickUpState(Enum):
    SYNCED=True
    NOT_SYNCED=False

class ContactBase(BaseModel):
    email: str
    firstname: str
    lastname: str
    phone: str
    website: str

class ContactRequest(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True

class HubspotContact(BaseModel):
    id: str
    properties: ContactRequest
