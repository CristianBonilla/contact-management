from fastapi import APIRouter

contact = APIRouter()

@contact.post('/contact')
def add_contact():
    return

@contact.get('/contact')
def sync_contacts():
    return
