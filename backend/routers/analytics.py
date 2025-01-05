from fastapi import APIRouter, HTTPException
from models.analytics import Analytics
from config import AppConfig, get_config
from typing import List

router = APIRouter()

config = AppConfig()


@router.get("/")
async def get_analytics():
    try:
        analytics_collection = config.db["Analytics"]
        data = await analytics_collection.find().to_list()
        models = []
        for i in data:
            models.append(i["modelName"])
            del i["_id"]

        return {"data": data, "models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
