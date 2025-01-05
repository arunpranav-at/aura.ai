import time
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from azure.storage.blob import BlobClient
from starlette.background import BackgroundTasks
from services.ai.rag.process import ingest_document
from services.ai.rag.response import process_query
from config import get_config, AppConfig
from helpers.filename import get_filename_hash
from models.rag import KnowledgeBaseUpload, KnowledgeBaseQuery


router = APIRouter()

config: AppConfig = get_config()


@router.post("/upload/document")
async def upload_document(file: UploadFile = File(...), username: str = Form(...)):
    # Get the file's content
    file_content = await file.read()

    # Create a Blob client and upload the file
    hashed_filename, digest = get_filename_hash(file.filename)
    blob_client: BlobClient = config.storage_container.get_blob_client(
        hashed_filename)

    blob_client.upload_blob(file_content, overwrite=True, metadata={
                            "username": username, "filename": file.filename, "id": digest})
    results = ingest_document(
        f"{config.env.knowledge_base_endpoint}{hashed_filename}")
    return {"status": "success", "message": "Document uploaded successfully."}


@router.post("/upload/text")
async def upload_text(content: KnowledgeBaseUpload):
    # Convert the text content into bytes
    file_content = content.content.encode("utf-8")

    # Get current Unix timestamp
    timestamp = int(time.time())
    file_name, digest = get_filename_hash(f"{timestamp}.txt")

    # Create a Blob client and upload the text
    blob_client = config.storage_container.get_blob_client(file_name)
    blob_client.upload_blob(file_content, overwrite=True, metadata={
                            "username": content.username, "filename": f"{timestamp}.txt", "id": digest})

    return {"status": "success", "message": "Text content uploaded successfully."}


@router.post("/response")
async def generate_response(query: KnowledgeBaseQuery):
    try:
        rag_response = process_query(query.query, query.username)
        rag_response = rag_response.get(
            "response", "Sorry, there are no relevant documents found for the query.")
        return {"bot_response": rag_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
