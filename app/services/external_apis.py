import httpx

async def fetch_data(name: str):
    async with httpx.AsyncClient() as client:
        g = client.get(f"https://api.genderize.io?name={name}")
        a = client.get(f"https://api.agify.io?name={name}")
        n = client.get(f"https://api.nationalize.io?name={name}")

        gender, age, nation = await g, await a, await n

    return gender.json(), age.json(), nation.json()


def validate(g, a, n):
    if g.get("gender") is None or g.get("count") == 0:
        raise Exception("Genderize returned an invalid response")

    if a.get("age") is None:
        raise Exception("Agify returned an invalid response")

    if not n.get("country"):
        raise Exception("Nationalize returned an invalid response")