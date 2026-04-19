# Stage 1 API — Profile Enrichment System

## Project Overview

This project is a backend API that accepts a name, retrieves demographic data from external APIs, applies classification logic, stores the result in a database, and exposes endpoints to manage profiles.

It demonstrates API integration, data persistence, idempotency handling, and REST API design.

---

## Tech Stack

- FastAPI  
- SQLModel  
- SQLite (local / Replit-friendly)  
- httpx (external API calls)  
- Uvicorn  
- Replit (deployment)

---

## External APIs Used

- Genderize API — gender prediction  
- Agify API — age prediction  
- Nationalize API — nationality prediction  

---

## Features

- Create profile using external APIs  
- Prevent duplicate entries using idempotency (by name)  
- Retrieve single profile by ID  
- Retrieve all profiles with optional filters:
  - gender
  - country_id
  - age_group  
- Delete profile by ID  

- Age classification:
  - 0–12 → child  
  - 13–19 → teenager  
  - 20–59 → adult  
  - 60+ → senior  

- Error handling for external API failures  
- CORS enabled for all origins  

---

## API Endpoints

### Create Profile
POST `/api/profiles`

Creates a profile using external API data.

---

### Get Single Profile
GET `/api/profiles/{id}`

Returns a single stored profile.

---

### Get All Profiles
GET `/api/profiles`

Optional filters:
- gender
- country_id
- age_group

Example:
`/api/profiles?gender=male&country_id=NG`

---

### Delete Profile
DELETE `/api/profiles/{id}`

Returns:
204 No Content

---

## Error Handling

All errors follow this format:

```json
{
  "status": "error",
  "message": "error description"
}
