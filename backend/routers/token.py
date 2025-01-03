import bson
from handlers.auth import decode_jwt
from config import AppConfig, get_config
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

config = AppConfig()


@router.get("/validate")
async def validate_token(request: Request) -> JSONResponse:
    if token := request.cookies.get("token"):
        decoded_token = decode_jwt(token)
        user = await config.db["User"].find_one(
            {"_id": bson.objectid.ObjectId(decoded_token["userid"])}
        )
        if not user:
            raise HTTPException(
                status_code=409,
                detail={"status": "failed", "message": "User not found"},
            )
        return {
            "user": {
                "name": user.get("username"),
                "id": decoded_token["userid"],
                "email": user.get("email"),
                "avatar": user.get("avatar"),
            }
        }
        return user
