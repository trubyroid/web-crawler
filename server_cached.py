from fastapi import FastAPI, status
from pydantic import BaseModel
import uvicorn
import uuid
import asyncio
import aiohttp
import redis
from urllib.parse import urlparse


class Response_running(BaseModel):
    status: str = "Running"
    id: uuid.UUID = None


class Response_ready(BaseModel):
    status: str = "Ready"
    result: dict = {}


class Request(BaseModel):
    urls: list = None


app = FastAPI()
request = Request()
response_result = {}
r = redis.Redis()
domains = []
counts = {}


async def counter():
    for i in request.urls:
        domain = urlparse(i).netloc
        if domain in domains:
            counts[domain] += 1
            print(f"\n{domain} was here {counts[domain]} times")
        else:
            domains.append(domain)
            counts[domain] = 1


@app.get("/")
async def read_root():
    return {"Hello": "Peer"}


@app.post("/api/v1/tasks/",
          status_code=status.HTTP_201_CREATED)
async def tasks(item: list):
    request.urls = item
    await counter()
    return Response_running(id=uuid.uuid4())


async def collecting():
    async with aiohttp.ClientSession() as session:
        for i in request.urls:
            async with session.get(i) as resp:
                response_result[i] = resp.status


@app.get("/api/v1/tasks/{data}",
         status_code=status.HTTP_201_CREATED)
async def tasks(data: str):
    await collecting()
    global response_result
    if response_result == {}:
        return Response_running(id=None)
    else:
        res = response_result
        response_result = {}
        return Response_ready(result=res)


async def server():
    uvicorn.run("server_cached:app", port=8888, reload=True, access_log=False)


if __name__ == "__main__":
    asyncio.run(server())

