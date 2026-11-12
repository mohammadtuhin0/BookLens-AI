import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend.app.api import health, books
from backend.app.core.config import settings
from backend.app.core.logging_config import logger
from backend.app.core.exceptions import BookLensException

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup
    logger.info("BookLens AI application is starting...")
    logger.info("Application version: %s", settings.APP_VERSION)

    yield

    # Application shutdown
    logger.info("BookLens AI application is shutting down...")


app = FastAPI(
    title=f"{settings.APP_NAME} API",
    description="An AI-powered visual book understanding and knowledge assistant.",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

@app.exception_handler(BookLensException)
async def booklens_exception_handler(
    request: Request,
    exc: BookLensException,
):
    logger.error(
        "Application error: %s | Code: %s",
        exc.message,
        exc.error_code,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
            },
        },
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    logger.warning(
        "HTTP error: %s | Path: %s",
        exc.detail,
        request.url.path,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "HTTP_ERROR",
                "message": str(exc.detail),
            },
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unexpected error occurred | Path: %s",
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred.",
            },
        },
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        logger.info(
            "%s %s | Status: %s | Duration: %.4f seconds",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )

        return response

    except Exception:
        process_time = time.perf_counter() - start_time

        logger.error(
            "%s %s | Unhandled exception | Duration: %.4f seconds",
            request.method,
            request.url.path,
            process_time,
        )

        raise


@app.get("/")
async def root():
    return {
        "message": "Welcome to BookLens AI",
        "status": "running",
        "version": settings.APP_VERSION,
    }


app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    books.router,
    prefix="/api/v1",
    tags=["Books"],
)



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    logger.warning(
        "Request validation failed | Path: %s",
        request.url.path,
    )

    errors = [
        {
            "field": ".".join(str(item) for item in error["loc"]),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed.",
                "details": errors,
            },
        },
    )
