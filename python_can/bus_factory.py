from __future__ import annotations

import can


def create_bus(interface: str = "virtual", channel: str = "aadi-demo") -> can.BusABC:
    """Create a software-only virtual bus by default.

    `socketcan` is supported for Linux software-only vcan testing.
    No physical interface is required by this package.
    """
    if interface == "socketcan":
        return can.Bus(interface="socketcan", channel=channel, receive_own_messages=False)

    # python-can virtual interface: pure software bus
    return can.Bus(interface="virtual", channel=channel, receive_own_messages=False)
