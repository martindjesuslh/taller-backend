from fastapi import APIRouter


from .auth.router import auth_router

api_router = APIRouter()

api_router_auth = api_router.include_router(auth_router)
