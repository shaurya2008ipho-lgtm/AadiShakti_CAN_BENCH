from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

import can
import cantools

from bus_factory import create_bus

ROOT = Path(__file__).resolve().parents[1]
DBC = cantools.database.load_file(str(ROOT / "dbc" / "aadi_shakti_demo.dbc"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Decode the Aadi-Shakti demo CAN traffic")
    parser.add_argument("--interface", default="virtual", choices=["virtual", "socketcan"])
    parser.add_argument("--channel", default="aadi-demo")
    parser.add_argument("--csv", default=str(ROOT / "can_capture.csv"))
    args = parser.parse_args()

    bus = create_bus(args.interface, args.channel)
    out = Path(args.csv)
    fields = ["timestamp", "id", "message", "signals"]

    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        print(f"Listening on {args.interface}:{args.channel}. Press Ctrl+C to stop.")
        try:
            while True:
                msg = bus.recv(timeout=1.0)
                if msg is None:
                    continue
                try:
                    decoded = DBC.decode_message(msg.arbitration_id, msg.data)
                    name = DBC.get_message_by_frame_id(msg.arbitration_id).name
                except Exception:
                    decoded = {"raw": msg.data.hex(" ")}
                    name = "UNKNOWN"

                row = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "id": hex(msg.arbitration_id),
                    "message": name,
                    "signals": decoded,
                }
                print(row)
                writer.writerow(row)
                f.flush()
        except KeyboardInterrupt:
            pass
        finally:
            bus.shutdown()


if __name__ == "__main__":
    main()
