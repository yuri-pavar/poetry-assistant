# from fastapi import FastAPI
# # from app.api.endpoints import router
# from app.api.endpoints_celery import router
# # from app.core.pipeline import get_pipeline
# from app.core import state


# # app = FastAPI(title="Poetry Assistant API")
# app = FastAPI(title="Poetry Assistant API", root_path="/api")
# # app = FastAPI(
# #     title="Poetry Assistant API",
# #     docs_url="/api/docs",
# #     redoc_url=None,
# #     openapi_url="/api/openapi.json"
# # )
# # app = FastAPI(
# #     title="Poetry Assistant API",
# #     docs_url="/docs",
# #     openapi_url="/openapi.json"
# # )
# # app.include_router(router, prefix="/api")
# app.include_router(router)

# # @app.on_event("startup")
# # async def startup_event():
# #     state.pipeline = get_pipeline()

# @app.get("/")
# async def root():
#     return {"message": "Poetry Assistant"}


from fastapi import FastAPI
from app.api.endpoints_celery import router

app = FastAPI(title="Poetry Assistant API", root_path="/api")
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Poetry Assistant"}