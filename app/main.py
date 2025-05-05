from fastapi import FastAPI
from app.api.endpoints import router
from app.core.pipeline import create_pipeline
from app.core import state


app = FastAPI(title="Poetry Assistant API")
app.include_router(router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    state.pipeline = create_pipeline()

@app.get("/")
async def root():
    return {"message": "Poetry Assistant"}