from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import numpy as np
import time
import threading
import multiprocessing

app = FastAPI()
generators = {}






def publish_sine(amp: float, freq: float):
    while True:
        for angle in range(0, 360):
            sin_value = amp * np.sin(np.deg2rad(angle))
            point = [{
                "measurement": 'sin',
                "fields": {"sin_value": sin_value}
            }]
            time.sleep(freq)


class SineGeneratorParams(BaseModel):
    amp: float
    freq: float


@app.post("/items/{item_id}")
async def create_generator(item_id: int, item: SineGeneratorParams):
    t = multiprocessing.Process(target=publish_sine, args=(item.amp, item.freq))
    t.start()
    generators[item_id] = t
    return {'item_id': item_id, 'works': generators[item_id].is_alive()}

@app.delete("/items/{item_id}")
async def delete_generator(item_id: int):
    generators[item_id].terminate()
    return {'item_id': item_id, 'works': generators[item_id].is_alive()}


@app.get("/items/")
async def get_generators():
    return {key: generators[key].is_alive() for key in generators.keys()}
