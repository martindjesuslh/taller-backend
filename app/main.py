from fastapi import FastAPI
from app.api.v1.routers import users

app = FastAPI(title="ADA Restauraciones API")

app.include_router(users.router, prefix="/api/v1", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Bienvenido a ADA Restauraciones API"}
