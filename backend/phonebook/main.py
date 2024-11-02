from fastapi import FastAPI, HTTPException
from uuid import UUID
from models.contact_base import Contact, Update_contact

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@hins.fdmah.mongodb.net/?retryWrites=true&w=majority&appName=hins"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = FastAPI()

contacts = []

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