# CAN Bench Architecture

```text
Mock sensor generator
       |
       | python-can
       v
Software CAN bus (virtual) ---> DBC decoder (cantools) ---> FastAPI/WebSocket ---> browser dashboard
```

The same DBC defines the message and signal layout for the simulator and decoder. This makes the demo reproducible and avoids presenting simulated data as real hardware telemetry.

## Demo sequence

1. Start the mock node.
2. Start the dashboard.
3. Show frames arriving live.
4. Switch the simulator fault profile from `normal` to `egt_rise` or `oil_drop` in a separate terminal.
5. Point out the corresponding telemetry changes in the dashboard.
6. Explain that a physical MCU/CAN-transceiver node is a later engineering stage.
