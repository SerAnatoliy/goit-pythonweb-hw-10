from sqlalchemy.orm import Session
from app.database.models import Contact
from app.database.schemas import ContactCreate, ContactUpdate

def get_contacts(db: Session):
    return db.query(Contact).all()

def get_contact_by_id(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone=contact.phone,
        birthday=contact.birthday,
        extra_info=contact.extra_info
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.dict(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact
