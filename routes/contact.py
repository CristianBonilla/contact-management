from fastapi import APIRouter

contact = APIRouter(prefix='/contact')

@contact.post('/')
def add():
    return

@contact.post('/sync')
def sync():
    return
