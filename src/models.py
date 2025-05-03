from pydantic import BaseModel


class Issue(BaseModel):
    title: str
    body: str | None = None


class File(BaseModel):
    path: str
    content: str 

class FileList(BaseModel):
    files: list[File]