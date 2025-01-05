from helpers import singleton
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from .environment import EnvVarConfig
from .database import get_database
from .rag import get_document_analysis_client, get_storage_client, get_rag_client, get_rag_search, get_rag_llm, get_blob_service_client


@singleton
class AppConfig():
    def __init__(self):
        self.env: EnvVarConfig = EnvVarConfig()
        self.db: AsyncIOMotorDatabase = get_database(self.env)
        self.blob_service_client = get_blob_service_client(
            self.env.azure_storage_account_connection_string)
        self.document_intelligence = get_document_analysis_client(
            self.env.document_intelligence_endpoint, self.env.document_intelligence_key)
        self.storage_container = get_storage_client(
            self.env.azure_storage_account_connection_string, self.env.kb_container_name)
        self.rag_container = get_storage_client(
            self.env.azure_storage_account_connection_string, self.env.rag_container_name)
        self.search = get_rag_search(
            self.env.ai_search_index_name, self.env.ai_search_api_key, self.env.ai_search_endpoint)
        self.llm = get_rag_llm(self.env.azure_openai_api_key, self.env.azure_openai_endpoint,
                               self.env.azure_openai_deployment, self.env.azure_openai_api_version)


def get_config():
    return AppConfig()
