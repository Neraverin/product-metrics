from pydantic import BaseModel


class APIConnection(BaseModel):
    api: str
    uuid: str
    secret: str
