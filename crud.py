from sqlmodel import select
from models import Profile

def get_profile_by_name(session, name):
    statement = select(Profile).where(Profile.name == name)
    return session.exec(statement).first()


def get_profile_by_id(session, id):
    statement = select(Profile).where(Profile.id == id)
    return session.exec(statement).first()


def get_all_profiles(session, gender=None, country_id=None, age_group=None):
    statement = select(Profile)

    if gender:
        statement = statement.where(Profile.gender == gender.lower())
    if country_id:
        statement = statement.where(Profile.country_id == country_id.upper())
    if age_group:
        statement = statement.where(Profile.age_group == age_group.lower())

    return session.exec(statement).all()


def create_profile(session, profile):
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


def delete_profile(session, profile):
    session.delete(profile)
    session.commit()