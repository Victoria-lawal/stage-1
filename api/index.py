from fastapi import FastAPI

app = FastAPI()

@app.get("/api/profiles")
def test():
    return {"status": "working"}