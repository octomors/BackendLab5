import uvicorn
from fastapi import FastAPI, Request
from config import settings
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from models import db_helper
from api import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from exceptions import AppException
from fastapi_pagination import add_pagination
from task_queue import broker
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    if not broker.is_worker_process:
        await broker.startup()

    yield
    # shutdown
    await db_helper.dispose()

    if not broker.is_worker_process:
        await broker.shutdown()


main_app = FastAPI(
    lifespan=lifespan,
)
main_app.include_router(
    api_router,
)
main_app.mount("/static", StaticFiles(directory="media"), name="static")

add_pagination(main_app)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["Authorization"],
    expose_headers=["X-File-Name"],
)


@main_app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
