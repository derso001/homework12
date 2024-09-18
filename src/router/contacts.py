from fastapi import Depends, HTTPException, status, Query, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from src.db.db import get_db
from src.db.models import Contact
from src.schemas import ContactCreate, ContactResponse


router =  APIRouter(prefix='/contact', tags=["contact"])

@router.post("/contacts")
async def create_note(contact: ContactCreate, db: Session = Depends(get_db)):
    new_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone_number=contact.phone_number,
        birthday=contact.birthday,
        additional_info=contact.additional_info)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


@router.get("/contacts")
async def read_contacts(skip: int = 0, limit: int = Query(default=10, le=100, ge=10), db: Session = Depends(get_db)):
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return contacts


@router.get("/contacts/search", response_model=List[ContactResponse])
async def search_contacts(
    first_name: Optional[str] = Query(None, description="Search by first name"),
    last_name: Optional[str] = Query(None, description="Search by last name"),
    email: Optional[str] = Query(None, description="Search by email"),
    db: Session = Depends(get_db)
):
    query = db.query(Contact)
    
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    
    contacts = query.all()
    return contacts


@router.get("/contacts/upcoming-birthdays", response_model=List[ContactResponse])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    today = datetime.today().date()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).filter(
        Contact.birthday.between(today, next_week)
    ).all()

    return contacts


@router.get("/contacts/{contact_id}")
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/contacts/{contact_id}")
async def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return None
