from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Response, Cookie
from fastapi.responses import RedirectResponse

from app.use_cases.auth_service import AuthService
from .dependencies import get_auth_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    auth_service: AuthService = Depends(get_auth_service),
):
    session = auth_service.authenticate(username=username, password=password)
    if session is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    redirect = RedirectResponse(url="/", status_code=302)
    redirect.set_cookie("session_id", session.id, httponly=True)
    return redirect


@router.post("/register")
async def register(
    username: str = Form(...),
    password: str = Form(...),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        auth_service.register(username=username, password=password)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex)) from ex
    return RedirectResponse(url="/", status_code=302)


@router.post("/logout")
async def logout(
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
    session_id: Optional[str] = Cookie(default=None, alias="session_id"),
):
    if session_id is not None:
        auth_service.logout(session_id)
    redirect = RedirectResponse(url="/", status_code=302)
    redirect.delete_cookie("session_id")
    return redirect
