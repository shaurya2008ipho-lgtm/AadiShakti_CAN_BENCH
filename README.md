# AADI-SHAKTI — CAN Communication & Telemetry Bench

> **Software-in-the-loop CAN telemetry demonstrator for the AADI-SHAKTI Digital Twin project**

AADI-SHAKTI — *The Shield of Indian Skies* — is an AI-enabled Digital Twin concept for health monitoring, fault prediction, degradation tracking, Remaining Useful Life (RUL) estimation, and mission reliability enhancement of aero-piston engines used in MALE UAVs.

This repository contains the **CAN communication and telemetry demonstration layer** developed as a software prototype for the hackathon. It provides a simulated engine telemetry source, CAN/DBC message representation, decoding/monitoring utilities, and a lightweight browser dashboard for observing the resulting telemetry.

The current implementation is intentionally **simulation-only**. It does not require physical sensors, a fabricated PCB, an aircraft ECU, or an operational UAV.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Why CAN Telemetry Matters](#why-can-telemetry-matters)
- [How This Repository Fits AADI-SHAKTI](#how-this-repository-fits-aadi-shakti)
- [Telemetry Parameters](#telemetry-parameters)
- [Repository Architecture](#repository-architecture)
- [Technology Stack](#technology-stack)
- [What Is Implemented](#what-is-implemented)
- [Current Development Limitations](#current-development-limitations)
- [Simulation Strategy](#simulation-strategy)
- [Running the Demonstrator](#running-the-demonstrator)
- [Demonstration Scenarios](#demonstration-scenarios)
- [Future Enhancements](#future-enhancements)
- [Relation to the Main GCS Repository](#relation-to-the-main-gcs-repository)
- [Project Philosophy](#project-philosophy)
- [Team / Hackathon Context](#team--hackathon-context)

---

## Project Overview

A Digital Twin is only useful when the virtual engine receives a continuous stream of meaningful engine-state information.

In the intended AADI-SHAKTI architecture, engine telemetry originates from sensors and embedded interfaces and is transported through a communication layer before reaching the Digital Twin and predictive-intelligence pipeline.

The intended high-level flow is:

```text
Engine Sensors / ECU
        ↓
CAN Communication Layer
        ↓
Telemetry Acquisition
        ↓
Data Decoding & Validation
        ↓
Digital Twin Core
        ↓
Physics + AI/ML + QML
        ↓
Health / Fault / Degradation / RUL
        ↓
GCS Dashboard
```

Because physical hardware was not available within the hackathon development window, this repository implements the telemetry portion as a **software-in-the-loop demonstrator**.

The goal is to preserve the architecture and demonstrate how the communication layer will behave once real hardware becomes available.

---

## Why CAN Telemetry Matters

CAN is a widely used communication approach for exchanging structured telemetry between embedded components. In the AADI-SHAKTI concept, the communication layer acts as the bridge between engine-state measurements and the higher-level Digital Twin software.

The repository therefore focuses on four practical ideas:

1. **Representing engine telemetry as structured messages**
2. **Encoding and decoding those messages using a DBC definition**
3. **Generating realistic simulated telemetry for development and testing**
4. **Providing monitoring tools that can later be connected to a real telemetry source**

The software is designed so that the simulation source can eventually be replaced by a real, approved test-bench or laboratory telemetry source without redesigning the higher-level data representation.

---

## How This Repository Fits AADI-SHAKTI

The larger AADI-SHAKTI ecosystem separates the project into functional layers:

```text
MISSION / ENGINEERING
        │
        ▼
Telemetry & Electronics
        │
        ├── Sensors / MCU / ECU interface
        ├── CAN / CAN transceiver
        ├── SocketCAN / python-can
        └── MQTT (where required)
        │
        ▼
DIGITAL TWIN CORE
        │
        ├── Expected engine behaviour
        ├── Observed telemetry
        └── Physics residuals
        │
        ▼
AI / PREDICTIVE INTELLIGENCE
        │
        ├── Classical ML
        ├── Fault classification
        ├── Degradation / RUL
        └── Experimental QML
        │
        ▼
GCS DASHBOARD
```

This repository concentrates on the **Telemetry & Electronics software layer**. The main GCS dashboard is maintained separately.

---

## Telemetry Parameters

The demonstrator is based on the engine parameters identified for the AADI-SHAKTI project:

| Parameter | Meaning | Prototype Role |
|---|---|---|
| RPM | Engine rotational speed | Engine operating state |
| CHT | Cylinder Head Temperature | Thermal health |
| EGT | Exhaust Gas Temperature | Combustion / thermal indication |
| Oil Pressure | Lubrication-system pressure | Lubrication health |
| Oil Temperature | Lubricant temperature | Thermal / lubrication health |
| Fuel Flow | Fuel consumption rate | Fuel-system behaviour |
| Vibration | Vibration level | Mechanical-condition indication |
| Battery | Electrical supply state | Electrical-system indication |
| Injection Timing | Injection timing parameter | Fuel / combustion behaviour |

These are **simulated values** in the current repository.

---

## Repository Architecture

```text
Aadi-Shakti-CANCommunicationBenchSimulator/
│
├── dashboard/
│   ├── app.py
│   └── static/
│       └── index.html
│
├── dbc/
│   └── aadi_shakti_demo.dbc
│
├── docs/
│   ├── CAN_BENCH_ARCHITECTURE.md
│   └── CAN_FRAME_MAP.md
│
├── python_can/
│   ├── __init__.py
│   ├── bus_factory.py
│   ├── mock_node.py
│   └── monitor.py
│
├── tests/
│   └── test_dbc.py
│
├── requirements.txt
├── run_demo_windows.bat
├── run_demo_linux.sh
└── README.md
```

### Directory responsibilities

#### `python_can/`

Contains the Python-side CAN abstraction and simulation utilities.

- `bus_factory.py` — creates/configures the software CAN interface used by the demonstrator.
- `mock_node.py` — generates simulated engine telemetry frames.
- `monitor.py` — receives/decodes telemetry for inspection.

#### `dbc/`

Contains the DBC definition used to describe how telemetry messages and signals are represented.

#### `dashboard/`

Contains a lightweight browser-based test interface for observing decoded telemetry independently from the main AADI-SHAKTI GCS.

#### `tests/`

Contains basic validation for the DBC/telemetry representation.

#### `docs/`

Contains architecture and frame-mapping notes intended to make future integration easier.

---

## Technology Stack

### Core software

- Python
- `python-can`
- `cantools`
- FastAPI
- HTML / CSS / JavaScript for the bench dashboard

### Communication / data concepts

- CAN message abstraction
- DBC message definitions
- Software-in-the-loop telemetry generation
- Telemetry decoding and monitoring

### Intended future hardware/tooling layer

The broader AADI-SHAKTI stack also anticipates:

- Sensors and MCU/ECU interface
- CAN transceiver hardware
- SocketCAN
- KiCad for electronics/PCB development
- LTspice / Proteus for electronics simulation
- Arduino IDE / PlatformIO for prototype firmware
- MQTT/Mosquitto for modular messaging where required

The physical hardware items are **not implemented in this repository yet**.

---

## What Is Implemented

The current software demonstrator provides:

### 1. Simulated telemetry source

A Python process generates representative engine telemetry without requiring physical sensors.

### 2. DBC-based representation

The telemetry is described using a DBC file so that signal names, message organization, and decoding can be kept explicit and version-controlled.

### 3. CAN monitoring path

The repository includes Python utilities for receiving and decoding the simulated messages.

### 4. Independent CAN test dashboard

A lightweight browser dashboard allows the development team to inspect telemetry values and message activity without depending on the main AADI-SHAKTI GCS.

### 5. Demonstration fault scenarios

The mock generator supports controlled abnormal-data scenarios so the team can demonstrate how telemetry changes under different simulated engine conditions.

### 6. Testable data layer

The DBC mapping is separated from the generator and monitor, making it easier to validate the data contract before connecting a real source.

---

## Current Development Limitations

This section is intentionally included for transparency in the hackathon submission.

### 1. Physical PCB was not fabricated

Due to the limited hackathon development time, the team could not complete fabrication and bench testing of a dedicated sensor/telemetry PCB.

The repository therefore uses a **software-only telemetry simulation** instead of claiming completed physical electronics integration.

### 2. Physical sensor arrangement was not completed

The intended system would acquire measurements from engine-related sensors and an appropriate embedded interface.

Because sufficient time was not available to prepare, install, calibrate, and validate a physical sensor arrangement, all telemetry values in the current demonstrator are simulated.

### 3. FlightGear → telemetry extraction was not completed

The broader AADI-SHAKTI concept includes FlightGear as the mission/flight simulation source. During the hackathon implementation window, the team did not complete the FlightGear-to-Python telemetry extraction and integration pipeline.

Therefore, this repository does **not** claim that the displayed CAN telemetry originates from live FlightGear data.

### 4. CAN bench was not connected to the main GCS

Due to the available development time, the standalone CAN telemetry demonstrator was not fully wired into the production data path of the main AADI-SHAKTI GCS dashboard.

The repository should therefore be viewed as a **separate validated communication-layer prototype** prepared for subsequent integration.

### 5. Hardware-level validation remains future work

The current implementation demonstrates software behaviour, not electrical or physical-bus validation. Hardware-in-the-loop testing, sensor calibration, physical bus validation, and bench-level qualification remain future development stages.

---

## Simulation Strategy

The philosophy behind the current prototype is:

> **Simulate the missing hardware honestly rather than presenting simulated data as physical telemetry.**

The software therefore keeps the simulated source clearly separated from the decoding and monitoring layers.

```text
                CURRENT HACKATHON DEMO

Mock Telemetry Generator
        │
        ▼
DBC-defined CAN Messages
        │
        ▼
CAN Monitor / Decoder
        │
        ▼
Test Dashboard
```

The intended final architecture is:

```text
                FUTURE INTEGRATION

Engine Sensors / Approved Test-Bench Source
        │
        ▼
MCU / ECU Interface
        │
        ▼
CAN Bus
        │
        ▼
CAN Acquisition Layer
        │
        ▼
AADI-SHAKTI Digital Twin
        │
        ▼
AI / ML / Experimental QML
        │
        ▼
Main GCS Dashboard
```

---

## Running the Demonstrator

### 1. Create a Python environment

From the repository root:

```bash
python -m venv .venv
```

### 2. Activate the environment on Windows

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the simulator

```powershell
python python_can\mock_node.py
```

The simulator can also be run with one of its supported demonstration scenarios.

### 5. Start the bench dashboard

In another terminal:

```powershell
python dashboard\app.py
```

Then open the local URL printed by the application in a browser.

### Important note for Windows

The current bench package was developed as a software demonstrator and uses a Python CAN abstraction intended for local testing. The exact behaviour of an in-memory/virtual CAN transport can depend on how the simulator and monitor processes are launched. For multi-process testing, the transport layer should be configured accordingly rather than assuming that all virtual-bus implementations share state across independent Python processes.

---

## Demonstration Scenarios

The CAN bench can be used to demonstrate the telemetry layer before the complete AADI-SHAKTI system is integrated.

### Normal engine condition

Typical simulated telemetry is generated for a stable operating state.

### Temperature rise

A simulated EGT/thermal trend can be introduced to demonstrate how abnormal thermal measurements would appear in the telemetry stream.

### Vibration increase

A simulated vibration increase can be used to demonstrate detection of a changing mechanical-condition signal.

### Combined abnormal telemetry

Multiple signals can be varied together to create a richer test case for later Digital Twin and AI/ML integration.

These scenarios are **simulation cases only** and are not intended to represent validated operational limits for a particular engine.

---

## Future Enhancements

The CAN repository is designed to grow into a hardware-backed telemetry subsystem.

### Phase 1 — Physical electronics prototype

- Complete a sensor-interface/telemetry PCB design in KiCad.
- Validate the electronics design in simulation where appropriate.
- Connect suitable bench sensors to a development MCU.
- Develop and validate embedded firmware for test-bench telemetry acquisition.

### Phase 2 — Bench CAN integration

- Introduce a physical CAN transceiver and controlled laboratory test-bench network.
- Validate physical message transmission and reception.
- Verify signal scaling and calibration against known test inputs.
- Replace the mock node with the real bench telemetry source while preserving the DBC contract.

### Phase 3 — FlightGear integration

- Establish a FlightGear telemetry extraction layer.
- Map mission/flight simulation variables to the AADI-SHAKTI telemetry schema.
- Synchronize simulated mission conditions with engine-state telemetry.
- Feed the resulting stream into the Digital Twin backend.

### Phase 4 — Main GCS integration

Connect the CAN telemetry layer to the main AADI-SHAKTI GCS so that:

```text
Telemetry
   ↓
Digital Twin
   ↓
Health Index
   ↓
Fault Classification
   ↓
RUL / Degradation
   ↓
GCS Visualization
```

can operate as one continuous data path.

### Phase 5 — Physics-informed intelligence

The telemetry layer can be combined with expected engine behaviour from the physics model so that residuals become useful diagnostic features.

### Phase 6 — AI/ML and experimental QML

Once an adequately sized and validated dataset exists:

- Establish a classical baseline.
- Add fault-classification models.
- Add degradation/RUL models.
- Perform explainability analysis.
- Evaluate experimental quantum-kernel or hybrid QML approaches on the same compact feature set.

Quantum methods should be treated as an experimental intelligence layer and should only be presented as advantageous when measured benchmarks support such a claim.

---

## Relation to the Main GCS Repository

The AADI-SHAKTI system is intentionally split into repositories/modules so that different subsystems can be developed independently.

```text
┌───────────────────────────────────────────────────────┐
│                  AADI-SHAKTI SYSTEM                  │
├───────────────────────────────────────────────────────┤
│                                                       │
│  CAN BENCH REPOSITORY                                 │
│  ├── Mock telemetry                                  │
│  ├── DBC definitions                                  │
│  ├── CAN monitoring                                  │
│  └── Communication-layer testing                     │
│                                                       │
│                      ↓ future integration             │
│                                                       │
│  MAIN GCS REPOSITORY                                  │
│  ├── React / TypeScript GCS                          │
│  ├── Digital Twin visualization                      │
│  ├── Engine health                                   │
│  ├── AI / ML                                          │
│  ├── Experimental QML                                │
│  ├── Mission tracking                                │
│  └── Mission replay                                  │
│                                                       │
└───────────────────────────────────────────────────────┘
```

The separation allows the communication subsystem to be tested independently before being attached to the complete Digital Twin application.

---

## Project Philosophy

AADI-SHAKTI is designed around the following principles:

### Predictive, not merely reactive

The system is intended to move from simple threshold monitoring toward combining observed telemetry, expected engine behaviour, anomaly detection, degradation tracking, and RUL estimation.

### Physics + data

Telemetry is most useful when it can be compared with expected engine behaviour. The larger architecture therefore treats physics-informed residuals as an additional intelligence signal.

### Modular architecture

The telemetry layer, Digital Twin, predictive intelligence, database, and GCS are separated so that individual components can evolve without requiring the entire system to be rebuilt.

### Honest prototyping

The current repository explicitly distinguishes simulated telemetry from future hardware integration. No physical sensor, PCB, FlightGear telemetry connection, or completed hardware validation is claimed here.

### Experimental quantum layer

Quantum ML is considered an experimental branch of the broader predictive-intelligence architecture rather than a replacement for the classical real-time Digital Twin backbone.

---



## Acknowledgement of Prototype Status

This repository is a **hackathon software prototype**. The current CAN layer demonstrates message representation, simulation, decoding, and monitoring in a controlled software environment.

The following remain planned integration stages:

- Physical PCB and electronics
- Physical sensor arrangement
- Laboratory/bench CAN validation
- FlightGear telemetry extraction
- Connection to the main AADI-SHAKTI GCS
- Larger validated datasets
- Production-grade model validation
- Integrated AI/ML and experimental QML pipeline

The purpose of the current repository is to establish a clear and testable foundation for those future steps.

---

## Final Vision

The long-term objective is a continuous telemetry-to-intelligence pipeline:

```text
                 AADI-SHAKTI

        Sensors / Mission Simulation
                    ↓
              CAN Telemetry
                    ↓
          Data Acquisition Layer
                    ↓
          Physics + Digital Twin
                    ↓
       ┌───────────┴───────────┐
       │                       │
 Classical ML              Experimental QML
       │                       │
       └───────────┬───────────┘
                   ↓
          Unified Engine Health
                   ↓
       Fault • Degradation • RUL
                   ↓
          Maintenance Advisory
                   ↓
             GCS Dashboard
```

**AADI-SHAKTI — Monitor. Analyse. Predict. Protect.**
