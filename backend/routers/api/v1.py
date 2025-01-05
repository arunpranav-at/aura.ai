import bson
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse

from config import AppConfig, get_config
from routers.auth import router as auth_router
from routers.chat import router as chat_router
from routers.bot import router as bot_router
from routers.test import router as test_model_router
from routers.rag import router as rag_router
from routers.analytics import router as analytics_router
from routers.token import router as token_router

from handlers.auth import decode_jwt


router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(chat_router, prefix="/chats")
router.include_router(bot_router, prefix="/bots")
router.include_router(rag_router, prefix="/rag")
router.include_router(test_model_router, prefix="/test-model")
router.include_router(analytics_router, prefix="/analytics")
router.include_router(token_router, prefix="/token")
