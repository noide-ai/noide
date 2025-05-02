from pydantic import BaseModel


class Issue(BaseModel):
    title: str
    body: str | None = None


class File:
    path: str
    content: str = ""
