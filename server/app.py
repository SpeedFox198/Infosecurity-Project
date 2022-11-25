from hypercorn import run
from quart import Quart, request, websocket
from quart_cors import cors
from functools import wraps
import socketio
import asyncio

from broker import Broker

DEBUG = True
PORT = 5000

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = Quart(__name__)
app = cors(app)
sio_app = socketio.ASGIApp(sio, app)

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

@sio.event
async def test(sid, data):
    print(f"Received data: {data}")
    await sio.emit("response", {"data":data["data"]})



# app.run(debug=DEBUG, port=PORT)  # Run app
# app.__class__.run(sio_app, debug=DEBUG, port=PORT)  # Run app
