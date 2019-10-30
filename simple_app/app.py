import pathlib
import fastapi
import uvicorn
import typing
# import pymongo # <- Uncomment to
import mongomock
import os
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse

# Import data models
from simple_app.models import LabMember, ApplicationSecret

## Create API Application
api = fastapi.FastAPI(version='1.0.0', description='A Simple API Application', title='Simple App')


# Add logo (because it's cool)
api.mount('/static/', StaticFiles(directory=pathlib.Path(__file__).parent / 'static'))

@api.get('/', include_in_schema=False)
async def root():
    return FileResponse(str(pathlib.Path(__file__).parent / 'static' / 'index.html'))

## Setup Databae Connection

# Setup database connection (Uncomment if database can be run)
try:
    client = pymongo.MongoClient(host='localhost',
        username=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        authSource='admin',
        authMechanism='SCRAM-SHA-256'
    )
except:
    raise RuntimeError('Failed to initialize database connection')

# client = mongomock.MongoClient().app_db # <-- Use if fake DB connection needed

## Declare Routes
@api.get("/members", response_model=typing.List[LabMember])
async def get_members():
    return list(client.labmembers.find())

@api.post("/members")
async def add_member(lm:LabMember):
    client.labmembers.update_one({'first': lm.first, 'last': lm.last}, {'$set': lm.dict()}, upsert=True)

    return lm.dict()

@api.get("/secret", response_model=ApplicationSecret)
async def get_secret():
    return {"secret": os.getenv('APP_SECRET', 'CHANGE-ME')}

# Execute Application
if __name__ == '__main__':
    uvicorn.run(api, host='0.0.0.0', port=9999)