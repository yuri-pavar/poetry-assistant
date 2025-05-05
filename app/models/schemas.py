from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str

class Output(BaseModel):
    query: str
    response: str

