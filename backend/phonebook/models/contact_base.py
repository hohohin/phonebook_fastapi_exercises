from pydantic import BaseModel, Field
from uuid import UUID

class Contact(BaseModel):
    id: UUID
    name : str = Field(min_length=1,max_length=10)
    number: str = Field(min_length=1,max_length=10)

class Update_contact(BaseModel):
    name : str | None = Field(min_length=1,max_length=10)
    number : str | None = Field(min_length=1,max_length=10)
