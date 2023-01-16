from pydantic import BaseModel
import uuid
import datetime


class Model(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    created_at: datetime.datetime = datetime.datetime.now()
    item: str
    content: str
