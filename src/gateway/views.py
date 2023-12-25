from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse

from src.gateway.containers import AuthContainer
from src.gateway.services.auth import AuthService

gateway_views = APIRouter()


@gateway_views.get('/login', include_in_schema=False)
@inject
async def login(request: Request, auth_service: AuthService = Depends(Provide[AuthContainer.auth_service])):
    access = await auth_service.get_auth(request)
    if access:
        return RedirectResponse("/profile")
    return FileResponse("templates/login.html", media_type="text/html")


@gateway_views.get('/register', include_in_schema=False)
@inject
async def register(request: Request, auth_service: AuthService = Depends(Provide[AuthContainer.auth_service])):
    access = await auth_service.get_auth(request)
    if access:
        return RedirectResponse("/profile")
    return FileResponse("templates/register.html", media_type="text/html")


@gateway_views.get('/profile', include_in_schema=False)
@inject
async def profile(request: Request, auth_service: AuthService = Depends(Provide[AuthContainer.auth_service])):
    access = await auth_service.get_auth(request)
    if not access:
        return RedirectResponse("/login")
    return FileResponse("templates/profile.html", media_type="text/html")

