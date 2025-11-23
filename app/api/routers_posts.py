from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.use_cases.blog_service import BlogService
from .dependencies import get_blog_service, get_current_user, CurrentUser


templates = Jinja2Templates(directory="app/web/templates")

router = APIRouter(tags=["posts"])


@router.get("/")
async def index(
    request: Request,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: Optional[CurrentUser] = Depends(get_current_user),
):
    posts = blog_service.list_recent_posts(limit=20)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "posts": posts, "current_user": current_user},
    )


@router.get("/posts/{post_id}")
async def post_detail(
    post_id: int,
    request: Request,
    blog_service: BlogService = Depends(get_blog_service),
    current_user: Optional[CurrentUser] = Depends(get_current_user),
):
    post = blog_service.get_post(post_id)
    if post is None:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(
        "post_detail.html",
        {
            "request": request,
            "post": post,
            "current_user": current_user,
        },
    )


@router.get("/new")
async def new_post_form(
    request: Request,
    current_user: Optional[CurrentUser] = Depends(get_current_user),
):
    if not current_user:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(
        "new_post.html",
        {"request": request, "current_user": current_user},
    )


@router.post("/posts")
async def create_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(default=None),
    blog_service: BlogService = Depends(get_blog_service),
    current_user: Optional[CurrentUser] = Depends(get_current_user),
):
    if not current_user:
        return RedirectResponse(url="/", status_code=302)

    image_filename: Optional[str] = None
    image_bytes: Optional[bytes] = None
    if image is not None:
        image_bytes = await image.read()
        if image_bytes:
            image_filename = image.filename

    blog_service.create_post(
        author_id=current_user.id,
        title=title,
        content=content,
        image_filename=image_filename,
        image_bytes=image_bytes,
    )
    return RedirectResponse(url="/", status_code=302)
