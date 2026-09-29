from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

import can
import cantools
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import sys
ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))

from python_can.bus_factory import create_bus

DBC = cantools.database.load_file(str(ROOT / "dbc" / "aadi_shakti_demo.dbc"))
app = FastAPI(title="Aadi-Shakti CAN Bench Dashboard")
app.mount("/static", StaticFiles(directory=str(Path(__file__).resolve().parent / "static")), name="static")

@app.get("/")
async def index():
    return FileResponse(Path(__file__).resolve().parent / "static" / "index.html")


def decode_message(msg: can.Message) -> dict:
    name = DBC.get_message_by_frame_id(msg.arbitration_id).name
    decoded = DBC.decode_message(msg.arbitration_id, msg.data)
    return {
        "timestamp": msg.timestamp,
        "id": hex(msg.arbitration_id),
        "message": name,
        "signals": decoded,
        "raw": msg.data.hex(" "),
    }


def get_bus(interface: str, channel: str):
    return create_bus(interface, channel)

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    interface = websocket.query_params.get("interface", "virtual")
    channel = websocket.query_params.get("channel", "aadi-demo")
    bus = get_bus(interface, channel)
    try:
        while True:
            msg = await asyncio.to_thread(bus.recv, 1.0)
            if msg is not None:
                await websocket.send_text(json.dumps(decode_message(msg), default=str))
            else:
                await websocket.send_text(json.dumps({"heartbeat": True}))
    except Exception:
        pass
    finally:
        bus.shutdown()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface", default="virtual", choices=["virtual", "socketcan"])
    parser.add_argument("--channel", default="aadi-demo")
    parser.add_argument("--port", type=int, default=8050)
    args = parser.parse_args()
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=args.port, reload=False)
