from fastapi import FastAPI, HTTPException
from uuid import UUID
import os
import uvicorn

# from models.contact_base import Contact, Update_contact
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field
from uuid import UUID

class Contact(BaseModel):
    id: UUID
    name : str = Field(min_length=1,max_length=10)
    number: str = Field(min_length=1,max_length=10)

class Update_contact(BaseModel):
    name : str | None = Field(min_length=1,max_length=10)
    number : str | None = Field(min_length=1,max_length=10)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

contacts = [
    {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "name": "string",
    "number": "string"
    }
]

@app.get("/api")
async def read_root():
    return {"Hello": "World"}

@app.get("/health")
def check_health():
    return "status healthy"

@app.get("/api/contacts")
def get_all_contacts():
    return contacts

@app.post("/api/contacts")
def create_contact(contact: Contact):
    contacts.append(contact)
    return "contact added"

@app.put("/api/contacts/{id}")
def update_contact(id:UUID,contact:Update_contact):
    i = 0
    for pre_contact in contacts:
        i += 1
        if pre_contact.id == id:
            if contact.name is not None:
                contacts[i-1].name = contact.name
            if contact.number is not None:
                contacts[i-1].number = contact.number
            return contacts[i-1]

    raise HTTPException(status_code=404, detail="person not found")

@app.delete("/api/contacts/{id}")
def delete_contact(id:UUID):
    for contact in contacts:
        if contact.id == id:
            contacts.remove(contact)
            return f"contact:{contact.name} deleted"
        
    raise HTTPException(status_code=404, detail="contact not found")

