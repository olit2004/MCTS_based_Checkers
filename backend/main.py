from fastapi import FastAPI
from .api.routes import router

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Checkers backend running"
    }

app.include_router(router)