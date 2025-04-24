from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import crud, schemas
from app.config import SessionLocal
from app.services.utils import search_contacts, get_upcoming_birthdays

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/contacts/", response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = crud.create_contact(db, contact)
    return db_contact

@router.get("/contacts/", response_model=list[schemas.ContactResponse])
def get_contacts(db: Session = Depends(get_db)):
    return crud.get_contacts(db)

@router.get("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact_by_id(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact(db, contact_id, contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.delete_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.get("/contacts/search/", response_model=list[schemas.ContactResponse])
def search_contacts_api(
    name: str = Query(None, description="Search by first or last name"),
    email: str = Query(None, description="Search by email"),
    db: Session = Depends(get_db),
):
    contacts = search_contacts(db, name, email)
    if not contacts:
        raise HTTPException(status_code=404, detail="No contacts found")
    return contacts

@router.get("/contacts/upcoming_birthdays/", response_model=list[schemas.ContactResponse])
def get_birthdays_api(db: Session = Depends(get_db)):
    contacts = get_upcoming_birthdays(db)
    if not contacts:
        raise HTTPException(status_code=404, detail="No upcoming birthdays found")
    return contacts
