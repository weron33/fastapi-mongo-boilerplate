from pydantic import BaseModel


class PostRequestBody(BaseModel):
    docs: list


class PutRequestBody(BaseModel):
    doc: dict


class QueryRequestBody(BaseModel):
    query: dict


class MigrateRequestBody(BaseModel):
    collections: list
