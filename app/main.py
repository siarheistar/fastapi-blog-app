from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.infrastructure.db import Base, engine
from app.api.routers_auth import router as auth_router
from app.api.routers_posts import router as posts_router


def create_app() -> FastAPI:
	Base.metadata.create_all(bind=engine)

	app = FastAPI(title="Blog App")

	static_dir = Path(__file__).resolve().parent / "web" / "static"
	app.mount("/static", StaticFiles(directory=static_dir), name="static")

	app.include_router(posts_router)
	app.include_router(auth_router)

	return app


app = create_app()
