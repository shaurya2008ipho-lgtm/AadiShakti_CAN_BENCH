from __future__ import annotations

import argparse
import math
import random
import time
from pathlib import Path

import can
import cantools

from bus_factory import create_bus

ROOT = Path(__file__).resolve().parents[1]
DBC = cantools.database.load_file(str(ROOT / "dbc" / "aadi_shakti_demo.dbc"))


def build_state(t: float, fault: str = "normal") -> dict[str, float]:
    rpm = 4500 + 120 * math.sin(t * 0.7)
    cht = 675 + 7 * math.sin(t * 0.23)
    egt = 815 + 14 * math.sin(t * 0.35)
    oil_p = 4.25 + 0.08 * math.sin(t * 0.4)
    oil_t = 112 + 2.5 * math.sin(t * 0.18)
    fuel = 31 + 0.8 * math.sin(t * 0.45)
    vibration = 2.0 + 0.15 * math.sin(t * 0.9) + random.uniform(-0.04, 0.04)
    battery = 27.6 + 0.1 * math.sin(t * 0.15)
    inj = 12.2 + 0.12 * math.sin(t * 0.25)

    if fault == "egt_rise":
        egt += 85
        cht += 25
    elif fault == "oil_drop":
        oil_p -= 1.15
        oil_t += 8
    elif fault == "vibration":
        vibration += 2.2
    elif fault == "injector":
        fuel += 5.0
        inj -= 1.4

    return {
        "rpm": rpm,
        "cht": cht,
        "egt": egt,
        "oil_pressure": oil_p,
        "oil_temp": oil_t,
        "fuel_flow": fuel,
        "vibration": vibration,
        "battery": battery,
        "injection_timing": inj,
    }


def send(bus: can.BusABC, name: str, values: dict[str, float]) -> None:
    message_def = DBC.get_message_by_name(name)
    payload = message_def.encode(values)
    bus.send(can.Message(arbitration_id=message_def.frame_id, data=payload, is_extended_id=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Aadi-Shakti software-only CAN sensor simulator")
    parser.add_argument("--interface", default="virtual", choices=["virtual", "socketcan"])
    parser.add_argument("--channel", default="aadi-demo")
    parser.add_argument("--fault", default="normal", choices=["normal", "egt_rise", "oil_drop", "vibration", "injector"])
    parser.add_argument("--period", type=float, default=0.1)
    args = parser.parse_args()

    bus = create_bus(args.interface, args.channel)
    print(f"CAN simulator running on {args.interface}:{args.channel}; fault={args.fault}")
    print("Simulation-only. Press Ctrl+C to stop.")

    t0 = time.monotonic()
    try:
        while True:
            t = time.monotonic() - t0
            state = build_state(t, args.fault)
            send(bus, "ENGINE_DYNAMICS", {"RPM": state["rpm"], "CHT": state["cht"], "EGT": state["egt"], "Vibration": state["vibration"]})
            send(bus, "LUBRICATION", {"OilPressure": state["oil_pressure"], "OilTemp": state["oil_temp"]})
            send(bus, "FUEL_ELECTRICAL", {"FuelFlow": state["fuel_flow"], "Battery": state["battery"], "InjectionTiming": state["injection_timing"]})
            time.sleep(args.period)
    except KeyboardInterrupt:
        pass
    finally:
        bus.shutdown()


if __name__ == "__main__":
    main()
