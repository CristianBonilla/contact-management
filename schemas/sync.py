from typing import List, Dict, Any
from sqlalchemy.orm import Session
from repositories.hubspot import Hubspot
from repositories.clickup import ClickUp
from schemas.contact import ContactBase, HubspotContact

class ApiCallHubspotToClickup:
    def __init__(self, endpoint: str, params: Dict[str, Any]):
        self._endpoint = endpoint
        self._params = params

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def params(self) -> Dict[str, Any]:
        return self._params

class HubspotToClickup:
    def __init__(
        self,
        session: Session,
        hubspot: Hubspot,
        clickup: ClickUp,
        api_call: ApiCallHubspotToClickup,
        data: List[Dict[str, Any]] = []):
        self._session = session
        self._hubspot = hubspot
        self._clickup = clickup
        self._api_call = api_call
        self._data = data

    @property
    def session(self) -> Session:
        return self._session

    @property
    def hubspot(self) -> Hubspot:
        return self._hubspot

    @property
    def clickup(self) -> ClickUp:
        return self._clickup

    @property
    def api_call(self) -> ApiCallHubspotToClickup:
        return self._api_call

    @property
    def data(self) -> List[Dict[str, Any]]:
        return self._data

    @property
    def contacts(self) -> List[HubspotContact]:
        return list(map(
            lambda contact : HubspotContact(
                id=contact['id'],
                properties=ContactBase(
                    email=contact['properties']['email'],
                    firstname=contact['properties']['firstname'],
                    lastname=contact['properties']['lastname'],
                    phone=contact['properties']['phone'],
                    website=contact['properties']['website']
                )
            ), self._data
        ))
