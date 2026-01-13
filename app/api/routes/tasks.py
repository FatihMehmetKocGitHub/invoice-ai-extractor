from fastapi import APIRouter
from app.storage.result_store import get_result

router = APIRouter()


@router.get("/tasks/{task_id}")
def get_task(task_id: str):
    result = get_result(task_id)
    if result is None:
        return {"status": "pending", "task_id": task_id}
    return {"status": "done", "task_id": task_id, "result": result}
