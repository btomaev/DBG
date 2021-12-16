#! /usr/bin/env python
# -*- coding: utf-8 -*-
from dbg_utils import *

setup()

def retry():
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(update("Retry")), loop.create_task(request(names,0))]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)


def nimoryan():
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(update("Nimoryan")), loop.create_task(request(names2,60))]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)

while True:
    loop = asyncio.get_event_loop()
    name = "Retry"
    tasks = [loop.create_task(update(name)), loop.create_task(request(names,60,name))]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)