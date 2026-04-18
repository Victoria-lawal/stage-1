Stage 1 Backend Wizards API

Project Overview
This project is a backend API that accepts a name, retrieves demographic data from external APIs, applies classification logic, stores the result in a database, and exposes endpoints to manage profiles.

Tech Stack
- FastAPI
- PostgreSQL (Neon)
- SQLModel
- Vercel (deployment)
- httpx (external API calls)

External APIs Used
- Genderize API
- Agify API
- Nationalize API

Features
- Create profile with external API integration
- Prevent duplicate entries using idempotency
- Retrieve single profile by ID
- Retrieve all profiles with filters (gender, country_id, age_group)
- Delete profile by ID
- Error handling for external API failures
- CORS enabled for all origins

API Endpoints

POST /api/profiles
Creates a profile using external API data.

GET /api/profiles/{id}
Retrieves a single profile.

GET /api/profiles
Retrieves all profiles with optional filters.

DELETE /api/profiles/{id}
Deletes a profile.

Error Handling
- 400: Missing or empty name
- 422: Invalid input type
- 404: Profile not found
- 502: External API failure

Deployment
The API is deployed on Vercel.

Local Setup
1. Install dependencies
2. Run uvicorn api.index:app --reload
3. Open http://127.0.0.1:8000/docs


git remote add origin https://github.com/Victoria-lawal/stage-1
git branch -M main
git push -u origin main