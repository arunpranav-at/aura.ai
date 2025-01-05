import time
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from azure.storage.blob import BlobClient
from starlette.background import BackgroundTasks
from services.ai.rag.process import ingest_document
from services.ai.rag.response import process_query
from config import get_config, AppConfig
from helpers.filename import get_filename_hash
from models.rag import KnowledgeBaseUpload, KnowledgeBaseQuery, KnowledgeBaseRetrieve


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


@router.post("/documents")
async def get_documents(payload: KnowledgeBaseRetrieve):
    matching_blobs = []
    try:
        for blob in config.storage_container.list_blobs():
            blob_name = blob.name
            blob_client = config.storage_container.get_blob_client(blob_name)
            # Get blob metadata
            metadata = blob_client.get_blob_properties().metadata

            # Check if the metadata contains the username key and value
            if 'username' in metadata and metadata['username'] == payload.username:
                file_path = f"{config.env.knowledge_base_endpoint}{blob_name}"
                rag_path = f"{config.env.rag_endpoint}{blob_name}"
                filename = metadata.get('filename')
                blob_id = blob_name.split(".")[0]
                matching_blobs.append(
                    {"file_path": file_path, "rag_path": rag_path, "filename": filename, "id": blob_id})
        return {"documents": matching_blobs}
    except Exception as e:
        return {"error": "Error retrieving files"}
