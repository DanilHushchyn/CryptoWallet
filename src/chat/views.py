from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse

from src.gateway.containers import AuthContainer
from src.gateway.services.auth import AuthService

chat_views = APIRouter()


@chat_views.get('/chat', include_in_schema=False)
@inject
async def chat(request: Request, auth_service: AuthService = Depends(Provide[AuthContainer.auth_service])):
    access = await auth_service.get_auth(request)
    if not access:
        return RedirectResponse("/login")
    return FileResponse("templates/chat.html", media_type="text/html")
