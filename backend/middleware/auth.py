import jwt
from typing import Dict, Optional, Callable
from config import AppConfig
from fastapi import Request, HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        if not (request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json") or request.url.path.startswith("/api/v1/auth")):
            token: Optional[str] = request.cookies.get("token")
            config = AppConfig()
            if token is None:
                response = await call_next(request)
                return response

            try:
                payload = jwt.decode(
                    token, config.env.jwt_secret, algorithms=["HS512"])
                request.state.user = payload

            except jwt.ExpiredSignatureError:
                raise HTTPException(
                    status_code=401, detail="JWT token has expired")

            except jwt.PyJWTError:
                raise HTTPException(
                    status_code=401, detail="JWT token is invalid")

            response = await call_next(request)

            return response

        response = await call_next(request)
        return response
