import os
from sqlmodel import create_engine
from dotenv import load_dotenv
from sqlmodel import SQLModel
from app.database import engine
from app.models import Profile

load_dotenv()  # 👈 THIS IS THE FIX

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
def init_db():
    SQLModel.metadata.create_all(engine)