from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
import uuid
from uuid6 import uuid7



def utc_now():
    return datetime.now(timezone.utc)


class Profile(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)
    name: str = Field(index=True, unique=True)

    gender: str
    gender_probability: float
    sample_size: int

    age: int
    age_group: str

    country_id: str
    country_probability: float

    created_at: datetime = Field(default_factory=utc_now)