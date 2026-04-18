from sqlmodel import Session, select
from app.models import Profile

def get_by_name(session, name):
    return session.exec(
        select(Profile).where(Profile.name == name)
    ).first()

def create(session, profile):
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile

def get_by_id(session, id):
    return session.get(Profile, id)

def get_all(session):
    return session.exec(select(Profile)).all()

def delete(session, profile):
    session.delete(profile)
    session.commit()