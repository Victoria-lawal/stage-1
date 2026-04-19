from pydantic import BaseModel

class CreateProfileRequest(BaseModel):
    name: str