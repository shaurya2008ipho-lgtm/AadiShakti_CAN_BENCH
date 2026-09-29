# Aadi-Shakti CAN Bench Simulator (Simulation-Only)

This package is a **bench/simulation-only CAN telemetry demonstrator** for the Aadi-Shakti hackathon prototype. It does not provide aircraft/vehicle control, actuator commands, or integration instructions for a real UAV.

## What it demonstrates

- `python-can` CAN bus abstraction
- `cantools` DBC encode/decode
- Mock engine sensor frames: RPM, CHT, EGT, oil pressure, oil temperature, fuel flow, vibration, battery, injection timing
- A local FastAPI dashboard showing decoded telemetry
- Fault-injection controls in the simulator (demo anomalies only)
- CAN frame logging to CSV
- Virtual CAN (`vcan0`) workflow on Linux, with a pure-software fallback for Windows
- DBC definition for the demo signals

The DBC file defines the signals and scaling; `cantools` supports loading DBC files and encoding/decoding CAN messages. `python-can` provides the bus abstraction used by the simulator.

## Quick start (Windows-friendly software-only mode)

1. `cd Aadi-Shakti-CAN-Bench-Simulator`
2. `python -m venv .venv`
3. `\.venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. `python python_can/mock_node.py`
6. In another terminal: `python dashboard/app.py`
7. Open http://127.0.0.1:8050

The mock node and dashboard use an in-memory software bus by default, so no CAN hardware is required.

## Linux vcan mode (optional)

Install SocketCAN tools for your Linux environment, create `vcan0`, and then run:

`python python_can/mock_node.py --interface socketcan --channel vcan0`

`python dashboard/app.py --interface socketcan --channel vcan0`

No physical CAN transceiver is required for `vcan0`; it is a software-only test bus.

## Project map

- `dbc/aadi_shakti_demo.dbc` — demo CAN network description
- `python_can/mock_node.py` — simulated sensor node
- `python_can/monitor.py` — decoded CAN monitor/logger
- `python_can/bus_factory.py` — in-memory or SocketCAN bus factory
- `dashboard/app.py` — FastAPI/WebSocket telemetry dashboard
- `dashboard/static/` — browser UI
- `tests/` — unit tests for scaling and DBC encode/decode
- `docs/CAN_BENCH_ARCHITECTURE.md` — bench architecture and demo script
- `docs/CAN_FRAME_MAP.md` — frame IDs and signal map

## Important scope


