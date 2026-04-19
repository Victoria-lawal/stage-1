import httpx

async def fetch_gender(name: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://api.genderize.io?name={name}")
        return res.json()

async def fetch_age(name: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://api.agify.io?name={name}")
        return res.json()

async def fetch_country(name: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://api.nationalize.io?name={name}")
        return res.json()