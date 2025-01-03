from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from handlers.test.model import test_model_handler
from handlers.test.matrix import matrix_handler

router = APIRouter()


class DataType(BaseModel):
    query: str
    response: str
    context: str
    result: str


@router.post("/")
async def test_model(data: DataType):
    try:
        query = data.query
        response = data.response
        context = data.context
        result = data.result
        result = await test_model_handler(query, response, context, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/matrix")
async def matrix():
    try:
        result = await matrix_handler()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
