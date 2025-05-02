from pydantic import BaseModel


class Issue(BaseModel):
    title: str
    body: str = ""


class File(BaseModel):
    path: str
    content: str = ""
