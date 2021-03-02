from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapi.handlers.register import register
from webapi.middleware.database_provider_middleware import \
    DatabaseProviderMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    DatabaseProviderMiddleware,
)

register(app)
