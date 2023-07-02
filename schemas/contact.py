from pydantic import BaseModel

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
