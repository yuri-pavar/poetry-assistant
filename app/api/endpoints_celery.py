from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest
from app.celery.tasks import generate_poetry_task
from app.celery.worker import celery_app

router = APIRouter()

@router.post("/generate_async")
async def generate_poetry_async(request: QueryRequest):
    task = generate_poetry_task.delay(request.query)
    return {"task_id": task.id, "status": "queued"}

@router.get("/result/{task_id}")
async def get_result(task_id: str):
    task_result = celery_app.AsyncResult(task_id)
    if task_result.state == "PENDING":
        return {"status": "pending"}
    elif task_result.state == "SUCCESS":
        return {"status": "completed", "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"status": "failed", "error": str(task_result.result)}
    else:
        return {"status": task_result.state}
