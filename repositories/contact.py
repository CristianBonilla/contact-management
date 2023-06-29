from sqlalchemy.orm import Session
from models.contact import Contact
from schemas.contact import ContactRequest

def add_contact(session: Session, contact_request: ContactRequest):
    contact = Contact(
        email=contact_request.email,
        firstname=contact_request.firstname,
        lastname=contact_request.lastname,
        phone=contact_request.phone,
        website=contact_request.website
    )
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact
