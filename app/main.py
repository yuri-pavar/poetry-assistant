from fastapi import FastAPI
from app.api.endpoints_celery import router


app = FastAPI(title="Poetry Assistant API", root_path="/api")
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Poetry Assistant"}