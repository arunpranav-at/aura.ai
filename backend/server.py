from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import AppConfig

from constants.middleware import cors_allowed_headers, cors_allowed_methods

from middleware.auth import JWTMiddleware

from routers.api.v1 import router as v1_router


app = FastAPI()

config = AppConfig()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.env.frontend_url],
    allow_methods=cors_allowed_methods,
    allow_headers=cors_allowed_headers,
    expose_headers=["*"],
    allow_credentials=True
)

app.add_middleware(JWTMiddleware)

app.include_router(v1_router, prefix="/api/v1")
