from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Yulia added this thing
# from api.router_socket import socket_router
from api.router_page import page_router
from auth.user import router
import logging
from datetime import datetime, timedelta
import jwt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

origins = ["*"] # Yulia added this thing

app = FastAPI(title="Medical Support")
# app.include_router(socket_router)
app.include_router(page_router)
app.include_router(router)

app.add_middleware( # Yulia added this thing |
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) # Yulia added this thing ^

