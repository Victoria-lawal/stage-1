from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import Session
from pydantic import BaseModel

from app.database import engine
from app.database import init_db
from app.models import Profile
from app.crud import get_by_name, create, get_by_id, get_all, delete
from app.services.external_apis import fetch_data, validate
from app.utils.classification import get_age_group

app = FastAPI()
init_db()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class ProfileRequest(BaseModel):
    name: str

# DB session
def get_session():
    with Session(engine) as session:
        yield session

# Formatter
def format_profile(p):
    return {
        "id": str(p.id),
        "name": p.name,
        "gender": p.gender,
        "gender_probability": p.gender_probability,
        "sample_size": p.sample_size,
        "age": p.age,
        "age_group": p.age_group,
        "country_id": p.country_id,
        "country_probability": p.country_probability,
        "created_at": p.created_at.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }

# POST /api/profiles
@app.post("/api/profiles", status_code=201)
async def create_profile(
    payload: ProfileRequest,
    session: Session = Depends(get_session)
):
    name = payload.name.strip().lower()

    if not name:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Missing or empty name"}
        )

    # Idempotency
    existing = get_by_name(session, name)
    if existing:
        return {
            "status": "success",
            "message": "Profile already exists",
            "data": format_profile(existing)
        }

    # External APIs
    try:
        g, a, n = await fetch_data(name)
        validate(g, a, n)
    except Exception:
        return JSONResponse(
            status_code=502,
            content={"status": "error", "message": "External API failure"}
        )

    # -------------------------
    # SAFE ACCESS (CRITICAL FIXES)
    # -------------------------

    gender = g.get("gender")
    gender_prob = g.get("probability", 0)
    gender_count = g.get("count", 0)

    age = a.get("age")

    countries = n.get("country", [])

    if not gender or gender_count == 0:
        return JSONResponse(
            status_code=502,
            content={"status": "error", "message": "Genderize returned an invalid response"}
        )

    if age is None:
        return JSONResponse(
            status_code=502,
            content={"status": "error", "message": "Agify returned an invalid response"}
        )

    if not countries:
        return JSONResponse(
            status_code=502,
            content={"status": "error", "message": "Nationalize returned an invalid response"}
        )

    top_country = max(countries, key=lambda x: x.get("probability", 0))

    # Create profile
    profile = Profile(
        name=name,
        gender=gender,
        gender_probability=gender_prob,
        sample_size=gender_count,
        age=age,
        age_group=get_age_group(age),
        country_id=top_country.get("country_id"),
        country_probability=top_country.get("probability", 0),
    )

    created = create(session, profile)

    return {
        "status": "success",
        "data": format_profile(created)
    }

# GET single profile
@app.get("/api/profiles/{id}")
def get_profile(id: str, session: Session = Depends(get_session)):
    profile = get_by_id(session, id)

    if not profile:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "message": "Profile not found"}
        )

    return {
        "status": "success",
        "data": format_profile(profile)
    }

# GET all profiles
@app.get("/api/profiles")
def get_profiles(
    gender: str = None,
    country_id: str = None,
    age_group: str = None,
    session: Session = Depends(get_session),
):
    profiles = get_all(session)

    if gender:
        profiles = [p for p in profiles if p.gender.lower() == gender.lower()]

    if country_id:
        profiles = [p for p in profiles if p.country_id.lower() == country_id.lower()]

    if age_group:
        profiles = [p for p in profiles if p.age_group.lower() == age_group.lower()]

    return {
        "status": "success",
        "count": len(profiles),
        "data": [
            {
                "id": str(p.id),
                "name": p.name,
                "gender": p.gender,
                "age": p.age,
                "age_group": p.age_group,
                "country_id": p.country_id,
            }
            for p in profiles
        ],
    }

# DELETE profile
@app.delete("/api/profiles/{id}", status_code=204)
def delete_profile(id: str, session: Session = Depends(get_session)):
    profile = get_by_id(session, id)

    if not profile:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "message": "Profile not found"}
        )

    delete(session, profile)
    return

from mangum import Mangum

handler = Mangum(app)