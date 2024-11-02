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

contacts = []

@app.get("/health")
def check_health():
    return "status healthy"

@app.get("/")
def get_all_contacts():
    return contacts

@app.post("/")
def create_contact(contact: Contact):
    contacts.append(contact)
    return "contact added"

@app.put("/{id}")
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

@app.delete("/{id}")
def delete_contact(id:UUID):
    for contact in contacts:
        if contact.id == id:
            contacts.remove(contact)
            return f"contact:{contact.name} deleted"
        
    raise HTTPException(status_code=404, detail="contact not found")


if __name__ == "__main__":
    # 使用环境变量获取端口，如果没有则默认使用 8000
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # 重要：使用 0.0.0.0 而不是 localhost
        port=port,
        reload=False  # 生产环境设置为 False
    )