from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from langchain_openai import AzureChatOpenAI


def get_blob_service_client(connection_string: str) -> BlobServiceClient:
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(
        connection_string)
    return blob_service_client

# Set up the Azure Form Recognizer client


def get_document_analysis_client(form_recognizer_endpoint: str, form_recognizer_key: str) -> DocumentAnalysisClient:
    document_analysis_client = DocumentAnalysisClient(
        endpoint=form_recognizer_endpoint,
        credential=AzureKeyCredential(form_recognizer_key)
    )
    return document_analysis_client


# Set up the Azure Blob Storage client
def get_storage_client(connection_string: str, container_name: str) -> BlobServiceClient:
    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string)
    container_client: ContainerClient = blob_service_client.get_container_client(
        container_name)
    return container_client


# Set up the Azure Blob Storage client
def get_rag_client(connection_string: str, rag_container_name: str) -> BlobServiceClient:
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(
        connection_string)
    rag_container_client: ContainerClient = blob_service_client.get_container_client(
        rag_container_name)
    return rag_container_client


def get_rag_search(index_name: str, api_key: str, ai_search_endpoint: str) -> SearchClient:
    search_client = SearchClient(
        endpoint=ai_search_endpoint, index_name=index_name, credential=AzureKeyCredential(api_key))
    return search_client


def get_rag_llm(openai_api_key: str, endpoint: str, deployment: str, api_version: str) -> AzureChatOpenAI:
    rag_llm = AzureChatOpenAI(
        openai_api_key=openai_api_key,
        azure_endpoint=endpoint,
        azure_deployment=deployment,
        api_version=api_version,
        temperature=0,
        max_tokens=5000,
        timeout=None,
        max_retries=2,
    )
    return rag_llm
