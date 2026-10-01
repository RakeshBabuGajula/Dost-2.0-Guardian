from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.workers import router as workers_router
from app.api.v1.trains import router as trains_router
from app.api.v1.work_zones import router as work_zones_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.near_misses import router as near_misses_router
from app.api.v1.devices import router as devices_router
from app.api.v1.emergency import router as emergency_router
from app.api.v1.system import router as system_router
from app.api.v1.websocket import router as websocket_router
from app.api.v1.spatial import router as spatial_router
from app.api.v1.simulation import router as simulation_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.ai_analytics import router as ai_analytics_router
from app.api.v1.integration import router as integration_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(workers_router)
api_v1_router.include_router(trains_router)
api_v1_router.include_router(work_zones_router)
api_v1_router.include_router(alerts_router)
api_v1_router.include_router(near_misses_router)
api_v1_router.include_router(devices_router)
api_v1_router.include_router(emergency_router)
api_v1_router.include_router(system_router)
api_v1_router.include_router(websocket_router)
api_v1_router.include_router(spatial_router)
api_v1_router.include_router(simulation_router)
api_v1_router.include_router(analytics_router)
api_v1_router.include_router(ai_analytics_router)
api_v1_router.include_router(integration_router)
