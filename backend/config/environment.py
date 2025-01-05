from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from helpers import singleton

load_dotenv()


@singleton
class EnvVarConfig(BaseSettings):
    environment: str
    cookie_domain: str
    api_domain: str
    frontend_url: str
    mongodb_uri: str
    mongodb_db: str
    jwt_secret: str
    bing_api_key: str
    bing_endpoint: str

    # Azure resources for RAG
    knowledge_base_endpoint: str
    azure_storage_account_connection_string: str
    kb_container_name: str
    rag_container_name: str
    ai_search_endpoint: str
    ai_search_api_key: str
    ai_search_index_name: str
    document_intelligence_endpoint: str
    document_intelligence_key: str

    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_deployment: str
    azure_openai_api_version: str

    # Credentials for OpenAI GPT-4o-mini's API key, endpoint, deployment, and API version environment variables
    azure_openai_api_key_gpt_4o_mini: str
    azure_openai_endpoint_gpt_4o_mini: str
    azure_openai_deployment_gpt_4o_mini: str
    azure_openai_api_version_gpt_4o_mini: str

    # Credentials for OpenAI GPT-4o's API key, endpoint, deployment, and API version environment variables
    azure_openai_endpoint_gpt_4o: str
    azure_openai_api_key_gpt_4o: str
    azure_openai_deployment_gpt_4o: str
    azure_openai_api_version_gpt_4o: str

    # Credentials for OpenAI GPT-4's API key, endpoint, deployment, and API version environment variables
    azure_openai_endpoint_gpt_4: str
    azure_openai_api_key_gpt_4: str
    azure_openai_deployment_gpt_4: str
    azure_openai_api_version_gpt_4: str

    # Credentials for OpenAI GPT-3.5-Turbo-16K API key, endpoint, deployment, and API version environment variables
    azure_openai_endpoint_gpt_35_turbo_16k: str
    azure_openai_api_key_gpt_35_turbo_16k: str
    azure_openai_deployment_gpt_35_turbo_16k: str
    azure_openai_api_version_gpt_35_turbo_16k: str

    azure_subscription_id: str
    azure_resource_group: str
    azure_project_name: str
    azure_client_id: str
    azure_tenant_id: str
    azure_client_secret: str

    class EnvVarConfig:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_env_config():
    return EnvVarConfig()
