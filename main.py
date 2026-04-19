from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Session

from db import engine, get_session
from schemas import CreateProfileRequest
import crud
import services
import utils
from models import Profile

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    print("SQLite DB ready")

    yield

    print("Shutdown")

app = FastAPI(lifespan=lifespan)
# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROOT CHECK
# =========================
@app.get("/")
def root():
    return {"message": "API is live"}


# =========================
# CREATE PROFILE
# =========================
@app.post("/api/profiles", status_code=201)
async def create_profile(
    request: CreateProfileRequest,
    session: Session = Depends(get_session)
):
    # -------------------------
    # 400: missing name
    # -------------------------
    if not request.name or request.name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "Missing or empty name"}
        )

    name = request.name.lower().strip()

    # -------------------------
    # idempotency check
    # -------------------------
    existing = crud.get_profile_by_name(session, name)
    if existing:
        return {
            "status": "success",
            "message": "Profile already exists",
            "data": existing
        }

    # -------------------------
    # external API calls
    # -------------------------
    try:
        gender_data = await services.fetch_gender(name)
        age_data = await services.fetch_age(name)
        country_data = await services.fetch_country(name)
    except Exception:
        raise HTTPException(
            status_code=502,
            detail={"status": "error", "message": "Upstream service failed"}
        )

    # =========================
    # 502 VALIDATIONS (STRICT)
    # =========================

    # Genderize
    if not gender_data.get("gender") or gender_data.get("count", 0) == 0:
        raise HTTPException(
            status_code=502,
            detail={
                "status": "error",
                "message": "Genderize returned an invalid response"
            }
        )

    # Agify
    if age_data.get("age") is None:
        raise HTTPException(
            status_code=502,
            detail={
                "status": "error",
                "message": "Agify returned an invalid response"
            }
        )

    # Nationalize
    if not country_data.get("country"):
        raise HTTPException(
            status_code=502,
            detail={
                "status": "error",
                "message": "Nationalize returned an invalid response"
            }
        )

    # =========================
    # PROCESS DATA
    # =========================
    age_group = utils.get_age_group(age_data["age"])
    top_country = utils.get_top_country(country_data["country"])

    profile = Profile(
        name=name,
        gender=gender_data["gender"],
        gender_probability=gender_data["probability"],
        sample_size=gender_data["count"],
        age=age_data["age"],
        age_group=age_group,
        country_id=top_country["country_id"],
        country_probability=top_country["probability"]
    )

    profile = crud.create_profile(session, profile)

    return {
        "status": "success",
        "data": profile
    }


# =========================
# GET SINGLE PROFILE
# =========================
@app.get("/api/profiles/{id}")
def get_profile(id: str, session: Session = Depends(get_session)):

    profile = crud.get_profile_by_id(session, id)

    if not profile:
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "message": "Profile not found"}
        )

    return {
        "status": "success",
        "data": profile
    }


# =========================
# GET ALL PROFILES (FILTERING)
# =========================
@app.get("/api/profiles")
def get_profiles(
    gender: str = None,
    country_id: str = None,
    age_group: str = None,
    session: Session = Depends(get_session)
):

    profiles = crud.get_all_profiles(session, gender, country_id, age_group)

    return {
        "status": "success",
        "count": len(profiles),
        "data": profiles
    }


# =========================
# DELETE PROFILE
# =========================
@app.delete("/api/profiles/{id}", status_code=204)
def delete_profile(id: str, session: Session = Depends(get_session)):

    profile = crud.get_profile_by_id(session, id)

    if not profile:
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "message": "Profile not found"}
        )

    crud.delete_profile(session, profile)