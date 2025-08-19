from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import os

from .database.connection import get_db, init_db
from .routers.auth import router as auth_router
from .routers.profile import router as profile_router
from .routers.avatar import router as avatar_router
from .routers.member import router as member_router
from .routers.invitation import router as invitation_router
from .routers.relationship import router as relationship_router
from .config.settings import settings
from .admin.config import create_admin
from .admin.basic_views import BasicUserAdmin, BasicAdminUserAdmin, BasicMemberAdmin, BasicUserProfileAdmin

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Mini Lively Backend", 
    version="1.0.0",
    description="A modular FastAPI backend with PostgreSQL database",
    lifespan=lifespan
)

# Add SessionMiddleware for OAuth (must be added first)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
app.include_router(avatar_router, prefix="/api")
app.include_router(member_router, prefix="/api")
app.include_router(invitation_router, prefix="/api")
app.include_router(relationship_router, prefix="/api")

# Create uploads directory and mount static files
uploads_dir = "uploads"
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Setup admin dashboard
admin = create_admin(app)
admin.add_view(BasicUserAdmin)
admin.add_view(BasicAdminUserAdmin)
admin.add_view(BasicMemberAdmin)
admin.add_view(BasicUserProfileAdmin)

@app.get("/")
async def root():
    return {"message": "Mini Lively Backend is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/db-test")
async def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute("SELECT 1")
        return {"database": "connected", "result": result.scalar()}
    except Exception as e:
        return {"database": "error", "message": str(e)}

@app.post("/seed-data")
async def seed_database_data(db: Session = Depends(get_db)):
    """Seed the database with default data (relationship types, etc.)"""
    try:
        from .crud.relationship_type import seed_default_relationship_types
        
        # Seed relationship types
        created_types = seed_default_relationship_types(db)
        
        result = {
            "success": True,
            "message": "Database seeded successfully",
            "created_relationship_types": len(created_types),
            "relationship_types": [
                {
                    "name": rel_type.name,
                    "display_name": rel_type.display_name,
                    "generation_offset": rel_type.generation_offset
                }
                for rel_type in created_types
            ]
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to seed database"
        }

@app.get("/relationship-types")
async def list_relationship_types(db: Session = Depends(get_db)):
    """List all relationship types in the database"""
    try:
        from .crud.relationship_type import get_all_relationship_types
        
        relationship_types = get_all_relationship_types(db, active_only=False)
        
        return {
            "success": True,
            "count": len(relationship_types),
            "relationship_types": [
                {
                    "name": rel_type.name,
                    "display_name": rel_type.display_name,
                    "generation_offset": rel_type.generation_offset,
                    "is_active": rel_type.is_active,
                    "is_reciprocal": rel_type.is_reciprocal
                }
                for rel_type in relationship_types
            ]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to fetch relationship types"
        }

# Test endpoints removed - backend is fully functional

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)