from pydantic import BaseModel

class Query(BaseModel):
    field: str
    operator: str
    value: str

class SearchQuery(BaseModel):
    query: Query