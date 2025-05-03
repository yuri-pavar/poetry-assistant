from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Poetry Assistant API")
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Poetry Assistant API is running."}