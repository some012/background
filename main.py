# main.py
import asyncio
from fastapi import FastAPI, Depends, Query
from datetime import datetime
from logging_config import configure_logger
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

async def background_task():
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"Текущее время: {current_time}")
        await asyncio.sleep(60)  # Запускать каждую минуту

@app.get("/get_time")
async def get_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    asyncio.create_task(background_task())
    return {"current_time": current_time}

def check_name(name: str = Query(None)):
    if name:
        return name
    else:
        return "Параметр отсутствует"

@app.get("/check")
def check_parameter(name: str = Depends(check_name)):
    return {"name": name}


class SetLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        import logging
        logging.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logging.info(f"Response: {response.status_code}")
        return response

configure_logger('requests.log')  # Указываем путь к файлу логов

app.add_middleware(SetLoggingMiddleware)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)