from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse

from src.gateway.containers import AuthContainer
from src.gateway.services.auth import AuthService

wallet_views = APIRouter()


@wallet_views.get('/wallets', include_in_schema=False)
@inject
async def wallets(request: Request, auth_service: AuthService = Depends(Provide[AuthContainer.auth_service])):
    access = await auth_service.get_auth(request)
    if not access:
        return RedirectResponse("/login")
    return FileResponse("templates/wallets.html", media_type="text/html")
