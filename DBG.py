from flask import Flask, request, redirect, url_for, render_template, abort
import json
from dbg_utils import *

app = Flask(__name__)

@app.route('/')
def settask():
    return open("Retry.html", "r").read()

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

def prt():
    print("djfdxcjfhy")

lp = asyncio.new_event_loop()
lp.run_until_complete(asyncio.gather(app.run(port=80, threaded=False)))

while True:
    loop = asyncio.get_event_loop()
    name = "Retry"
    tasks = [loop.create_task(update(name)), loop.create_task(request(names,60,name))]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)
    
    # prt()
