from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from .dependencies import get_db, init_db

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)