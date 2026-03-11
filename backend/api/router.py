from fastapi import APIRouter
from backend.api.endpoints import upload, activities, stats, export, agent

api_router = APIRouter()

api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])
api_router.include_router(activities.router, prefix="/activities", tags=["Activities"])
api_router.include_router(stats.router, prefix="/stats", tags=["Stats"])
api_router.include_router(export.router, prefix="/export", tags=["Export"])
api_router.include_router(agent.router, prefix="/agent", tags=["Agent"])

@api_router.get("/")
def root():
    return {"message": "Welcome to Nexus Sports API"}
