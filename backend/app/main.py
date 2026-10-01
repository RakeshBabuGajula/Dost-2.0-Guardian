import uuid
import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.api.v1.router import api_v1_router
from app.db.session import engine, Base
from app.db.init_db import init_seed_data

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] [CorrID: %(correlation_id)s] %(name)s: %(message)s",
)

class CorrelationLogFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "correlation_id"):
            record.correlation_id = "sys-core"
        return True

logger = logging.getLogger("dost_guardian.main")
logger.addFilter(CorrelationLogFilter())

app = FastAPI(
    title="DOST Guardian 2.0 Safety & Railway Intelligence Platform API",
    description="Production-ready FastAPI backend supporting PostGIS spatial queries, deterministic SafetyEngine, AI analytics, and authorized railway integration adapters.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Correlation ID & Security Headers Middleware
@app.middleware("http")
async def add_correlation_and_security_headers(request: Request, call_next):
    corr_id = request.headers.get("X-Correlation-ID") or request.headers.get("X-Request-ID") or f"corr-{uuid.uuid4().hex[:8]}"
    request.state.correlation_id = corr_id

    response = await call_next(request)

    response.headers["X-Correlation-ID"] = corr_id
    response.headers["X-Request-ID"] = corr_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# Global Exception Handler
@app.exception_handler(Exception)
async def custom_global_exception_handler(request: Request, exc: Exception):
    corr_id = getattr(request.state, "correlation_id", "unknown-corr-id")
    logger.error(f"Unhandled server exception [CorrID: {corr_id}]: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected application error occurred. Stack traces are suppressed in production.",
                "request_id": corr_id,
                "correlation_id": corr_id,
                "details": {},
            }
        },
    )

# Mount API V1 Router
app.include_router(api_v1_router)

@app.on_event("startup")
def on_startup():
    logger.info("Initializing database tables and seed data...", extra={"correlation_id": "startup"})
    try:
        Base.metadata.create_all(bind=engine)
        init_seed_data()
        logger.info("DOST Guardian 2.0 Backend initialized successfully with production security & observability headers.", extra={"correlation_id": "startup"})
    except Exception as e:
        logger.warning(f"Database initialization deferred or offline fallback: {e}", extra={"correlation_id": "startup"})
