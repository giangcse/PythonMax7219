import json
import os
import uvicorn

from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

class API:
    def __init__(self) -> None:
        # Khởi tạo API
        self.app = FastAPI()
        self.templates = Jinja2Templates(directory="templates/")
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )

        @self.app.get("/")
        async def root(request: Request):
            return self.templates.TemplateResponse('index.html', context={'request': request})

        @self.app.post("/")
        async def show(request: Request, noidung: str = Form(...), speed: int = Form(...), invert: bool = Form(False)):
            print(noidung, speed, invert)
            return self.templates.TemplateResponse('index.html', context={'request': request, 'result': 'Thiết lập thành công'})

        @self.app.post("/off")
        async def off(request: Request):
            return self.templates.TemplateResponse('index.html', context={'request': request})

api = API()

if __name__=='__main__':
    uvicorn.run('main:api.app', host='0.0.0.0', port=88, reload=True)