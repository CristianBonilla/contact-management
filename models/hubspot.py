from enum import Enum
from schemas.contact import ContactRequest

class ClickupState(Enum):
    SYNCED=True
    NOT_SYNCED=False

class HubspotContact:
    def __init__(self, id: str, properties: ContactRequest):
        self._id = id
        self._properties = properties

    @property
    def id(self) -> str:
        return self._id

    @property
    def properties(self) -> ContactRequest:
        return self._properties
