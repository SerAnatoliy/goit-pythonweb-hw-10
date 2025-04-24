from fastapi import FastAPI
from app.routes import contacts

app = FastAPI(title="Contacts API")

app.include_router(contacts.router)

@app.get("/")
def root():
    return {"message": "Welcome to Contacts API"}
