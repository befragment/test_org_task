from fastapi import FastAPI
from routers import organization

app = FastAPI()

app.include_router(organization.router)
