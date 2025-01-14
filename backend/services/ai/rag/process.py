import os
import logging
import mimetypes
import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_community.callbacks import get_openai_callback
from config import get_config

config = get_config()


def process_document(file_path: str):
    """
    Process the document from the given file path using Azure Form Recognizer (Document Intelligence).

    :param file_path: Path to the file (local or URL to the Blob).
    :return: Extracted content from the document.
    """

    file_name = file_path.split("/")[-1]
    blob_client = config.blob_service_client.get_blob_client(
        container=config.env.kb_container_name, blob=file_name)
    properties = blob_client.get_blob_properties()
    content_type, _ = mimetypes.guess_type(file_path)

    metadata = properties.metadata
    username = metadata.get("username")
    filename = metadata.get("filename")
    blob_id = metadata.get("id")

    # Process the document using Azure Document Intelligence (Form Recognizer)
    try:
        if content_type in ["application/pdf", "image/png", "image/jpeg"]:
            poller = config.document_intelligence.begin_analyze_document_from_url(
                "prebuilt-layout", file_path)
            result = poller.result()

            # Loop through the pages and extract text lines
            extracted_text = []
            for page in result.pages:
                for line in page.lines:
                    extracted_text.append(line.content)

            # Return the extracted content as a list of lines
            return {"id": blob_id, "content": "\n".join(extracted_text), "username": username, "metadata_file_path": file_path, "metadata_filename": filename}
        elif content_type == "text/plain":
            blob_data = blob_client.download_blob().readall().decode("utf-8")
            return {"id": blob_id, "content": blob_data, "username": username, "metadata_file_path": file_path, "metadata_filename": filename}
        else:
            return None
    except Exception as e:
        logging.error(f"Error processing the document: {e}")
        return None


def upload_rag_document(contents: dict):
    """
    Upload the processed document content to the RAG (Retrieval-Augmented Generation) container in Azure Blob Storage.

    :param contents: The processed document content.
    :return: The status of the upload.
    """
    try:
        blob_id = contents.get("id")
        content = contents.get("content")
        username = contents.get("username")
        metadata_file_path = contents.get("metadata_file_path")
        metadata_filename = contents.get("metadata_filename")
        file_name = f"{blob_id}.json"
        data = json.dumps(contents)

        blob_client = config.rag_container.get_blob_client(file_name)

        blob_client.upload_blob(data, overwrite=True, metadata={
                                "username": username, "filename": metadata_filename})

        return {"status": "success", "message": "Document uploaded to RAG successfully."}

    except Exception as e:
        logging.error(f"Error uploading document to RAG: {e}")
        return {"status": "error", "message": "Failed to upload document to RAG."}


def ingest_document(file_path: str):
    """
    Ingest the document from the given file path by processing and uploading it to the RAG container.

    :param file_path: Path to the file (local or URL to the Blob).
    :return: The status of the ingestion process.
    """
    processed_content = process_document(file_path)
    if processed_content:
        index_result = config.search.upload_documents([processed_content])
        upload_status = upload_rag_document(processed_content)
        return upload_status
    else:
        return {"status": "error", "message": "Failed to process the document."}
