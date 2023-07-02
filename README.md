# Contact Management

Rest API using FastAPI that allows contact creation in HubSpot and syncing with ClickUp, while also creating records in a PostgreSql database to log each API call

## Prerequisites

You will need the following things properly installed on your computer.

* [git](http://git-scm.com/)
* [python](https://www.python.org/)
* [anaconda](https://www.anaconda.com/)

### Installation

[![git](https://img.shields.io/badge/git-v2.x.x-orange.svg)](https://git-scm.com/downloads/)
[![python](https://img.shields.io/badge/python-v3.11.x-blue.svg)](https://www.python.org/downloads/)
[![anaconda](https://img.shields.io/badge/anaconda-v23.5.0-green.svg)](https://www.anaconda.com/download)

## Commands to configure virtual environment

1. `conda update -n base -c defaults conda`
2. `conda config --add channels conda-forge`
3. `conda config --show channels`
4. `conda create --name contact-management python=3`
5. `conda activate contact-management`
6. `conda deactivate`

## Environment List

| Name | Description |
| :---: | :--- |
| dev | **Development** environment

## Development server

Run `uvicorn main:app --reload` for a dev server. Navigate to <http://127.0.0.1:8000/> The application will automatically reload if you change any of the source files.

## Endpoints

| Name | Description |
| :--- | :--- |
| `/contact` | Add a new **contact**
| `/contact/sync` | Contacts added in **Hubspot** sync with **ClickUp** in background tasks

### `/contact` body endpoint

```json
{
  "email": "cris-boni@gmail.com",
  "firstname": "Cristian Camilo",
  "lastname": "Bonilla",
  "phone": "3261515501",
  "website": "https://github.com/CristianBonilla"
}
```

## API Docs (Swagger OpenAPI Specification)

Navigate to <http://127.0.0.1:8000/docs/>
