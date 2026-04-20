from fastapi import APIRouter
from app.api.v1.endpoints import login, partners, projects, tasks, timeboxing, compliance, lookups

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(lookups.router, prefix="/lookups", tags=["lookups"])
api_router.include_router(partners.router, prefix="/partners", tags=["partners"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(timeboxing.router, prefix="/timeboxing", tags=["timeboxing"])
api_router.include_router(compliance.router, prefix="/compliance", tags=["compliance"])
