from pydantic import BaseModel


class KnowledgeBaseUpload(BaseModel):
    username: str
    content: str


class KnowledgeBaseQuery(BaseModel):
    username: str
    query: str


class KnowledgeBaseRetrieve(BaseModel):
    username: str
