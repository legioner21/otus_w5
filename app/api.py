import random
import time

from fastapi import APIRouter

app_router = APIRouter()


@app_router.get("/method-1", summary="method-1")
def method_1():
    time.sleep(random.randint(1, 10))
    if random.choice([True, False]):
        raise Exception("test exception")
    return True


@app_router.post("/method-2", summary="method-2")
def method_2():
    time.sleep(random.randint(1, 2))
    if random.choice([True, False]):
        raise Exception("test exception")
    return True


@app_router.delete("/method-3", summary="method-3")
def method_3():
    time.sleep(random.randint(3, 5))
    if random.choice([True, False]):
        raise Exception("test exception")
    return True


api_router = APIRouter()
api_router.include_router(app_router, prefix="/app", tags=["app"])
