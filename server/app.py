from quart import Quart, request, websocket
from quart_cors import cors
from functools import wraps
import asyncio

from broker import Broker

DEBUG = True
PORT = 5000

app = Quart(__name__)
app = cors(app)

broker = Broker()

async def _receive() -> None:
    while True:
        message = await websocket.receive()
        await broker.publish(message)

@app.websocket("/ws")
async def ws() -> None:
    try:
        task = asyncio.ensure_future(_receive())
        async for message in broker.subscribe():
            await websocket.send(message)
    finally:
        task.cancel()
        await task

app.run(debug=DEBUG, port=PORT)  # Run app
