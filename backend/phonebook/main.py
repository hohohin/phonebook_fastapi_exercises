from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4
import logging

# from models.contact_base import Contact, Update_contact
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field
from uuid import UUID

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Create_contact(BaseModel):
    name : str = Field(min_length=1,max_length=10)
    number: str = Field(min_length=1,max_length=10)

class Contact(Create_contact):
    id : UUID

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

@app.get("/health")
def check_health():
    return "status healthy"

@app.get("/api/contacts")
def get_all_contacts():
    return contacts

@app.get("/api/contacts/{id}")
def get_the_contact(id):
    for contact in contacts:
        if contact["id"] == id:
            return contact
        raise HTTPException(status_code=404, detail="contact not found")

@app.post("/api/contacts")
def create_contact(contact: Create_contact):
    id_gen = uuid4()
    contact = {
        "id":id_gen,
        "name":contact.name,
        "number": contact.number
    }
    contacts.append(contact)
    return "contact added"

@app.put("/api/contacts/{id}")
def update_contact(id:UUID,contact:Update_contact):
    i = 0
    for pre_contact in contacts:
        i += 1
        if pre_contact["id"] == id:
            if contact.name is not None:
                contacts[i-1]["name"] = contact.name
            if contact.number is not None:
                contacts[i-1]["number"] = contact.number
            return contacts[i-1]

    raise HTTPException(status_code=404, detail="person not found")

@app.delete("/api/contacts/{id}")
def delete_contact(id:UUID):
    for contact in contacts:
        if contact["id"] == id:
            contacts.remove(contact)
            return f"contact:{contact["name"]} deleted"
        
    raise HTTPException(status_code=404, detail="contact not found")

