from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str

class QueryRequestQuote(BaseModel):
    query: str
    k: int

class Output(BaseModel):
    query: str
    response: str

