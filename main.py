#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import json
import os
import uvicorn
import re
import time
import argparse
import datetime

from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

from lunardate import LunarDate

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
        # Khởi tạo thiết bị Max7219
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(serial, cascaded=8, block_orientation=-90, rotate=0, blocks_arranged_in_reverse_order=False)

        @self.app.get("/")
        async def root(request: Request):
            return self.templates.TemplateResponse('index.html', context={'request': request})

        @self.app.post("/")
        async def show(request: Request, noidung: str = Form(...), speed: int = Form(...)):
            self.info(content=noidung, speed=speed)
            return self.templates.TemplateResponse('index.html', context={'request': request, 'result': 'Thiết lập thành công'})

        @self.app.post("/off")
        async def off(request: Request):
            self.info(content=None, speed=0)
            return self.templates.TemplateResponse('index.html', context={'request': request})

    def add_zero(self, number):
        if(int(number) < 10):
            return str(0) + str(number)
        else:
            return str(number)

    def day_of_week(self, date):
        if date==1:
            return 'T2'
        elif date==2:
            return 'T3'
        elif date==3:
            return 'T4'
        elif date==4:
            return 'T5'
        elif date==5:
            return 'T6'
        elif date==6:
            return 'T7'
        else:
            return 'CN'

    def info(self, content, speed):
        show_message(device, datetime.datetime.now().strftime("%H:%M"), fill="white", font=proportional(CP437_FONT), scroll_delay=0.05)
        time.sleep(1)
        dtime = self.day_of_week(int(datetime.datetime.now().isoweekday())) + ', ' + datetime.datetime.now().strftime("%d - %m - %Y")
        show_message(device, dtime, fill="white", font=proportional(SINCLAIR_FONT), scroll_delay=0.03)
        # Get lunar calendar
        lunar = LunarDate.fromSolarDate(int(datetime.datetime.now().strftime('%Y')), int(datetime.datetime.now().strftime('%m')), int(datetime.datetime.now().strftime('%d')))
        lunar_date = self.add_zero(lunar.day) + ' - ' + self.add_zero(lunar.month) + ' - ' + str(lunar.year) + ' (AL)'
        show_message(device, lunar_date, fill="white", font=proportional(SINCLAIR_FONT), scroll_delay=0.03)
        if content is not None:
            show_message(device, content, fill="white", font=proportional(SINCLAIR_FONT), scroll_delay=float(speed))

api = API()

if __name__=='__main__':
    uvicorn.run('main:api.app', host='0.0.0.0', port=80, reload=True)