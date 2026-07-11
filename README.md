# 400km Drone Test — HF Radio Communication Simulator

**A long-range (400 km) drone communication simulator that models an HF (High Frequency) radio channel in the 2–5 MHz range, with telemetry protocol and jamming filtering.**

## 📡 Description

This simulator models communication between a drone and a ground station over a 400 km distance:

- **HF radio channel** — on 2, 3, 4, 5 MHz frequencies
- **Real-time simulation** — 5-second communication cycles
- **Jamming simulation** — toggle jamming on individual frequencies
- **Telemetry protocol** — structured data packet transmission
- **Interactive control** — keyboard-driven (jamming on/off)

### Core Components

| Component | File | Description |
|-----------|------|-------------|
| Drone | `drone.py` | Drone-side transceiver and telemetry sender |
| Ground Station | `ground_station.py` | Ground receiver and command sender |
| Radio Channel | `radio_channel.py` | HF channel model with fading and noise |
| Protocol | `telemetry_protocol.py` | Packet format and data structure |
| Main Program | `main.py` | Interactive simulator |

## 📁 File Structure

```
400km dron test/
├── main.py                      # Main program — interactive simulator
├── drone.py                     # Drone-side logic
├── ground_station.py            # Ground station
├── radio_channel.py             # HF radio channel model
├── telemetry_protocol.py        # Telemetry protocol
├── automated_test.py            # Automated test
├── uav_swarm_designer.py        # Drone swarm designer
├── uav_design_output.py         # Design output
├── drone_preview.html           # Drone visualization (HTML)
├── uav_final_spec.json          # Final specification
└── README.md
```

## 🚀 Usage

### Launch interactive simulator

```bash
python main.py
```

### Commands

| Key | Action |
|-----|--------|
| `2` | Enable jamming on 2 MHz |
| `3` | Enable jamming on 3 MHz |
| `4` | Enable jamming on 4 MHz |
| `5` | Enable jamming on 5 MHz |
| `c` | Clear all jamming |
| `q` | Quit |

### Automated test

```bash
python automated_test.py
```

### Drone swarm designer

```bash
python uav_swarm_designer.py
```

### Sample output

```
==================================================
 DRONE HF COMMUNICATION SIMULATOR (2–5 MHz)
==================================================
 Commands:
  '2', '3', '4', '5' - Toggle jamming
  'c'                - Clear all jamming
  'q'                - Quit
==================================================

[2.0 MHz] Drone → Ground: OK | SNR: 12.3 dB
[3.0 MHz] Drone → Ground: JAMMING!! | SNR: -5.2 dB
[4.0 MHz] Drone → Ground: OK | SNR: 10.8 dB
[5.0 MHz] Drone → Ground: OK | SNR: 9.1 dB
```

## 📦 Dependencies

```bash
pip install numpy
```

- **Python 3.8+**
- **numpy** — signal processing and fading simulation
- **msvcrt** (Windows standard library) — keyboard monitoring

## 🔬 Simulation Model

### Radio Channel Parameters

- **Frequency:** 2–5 MHz (HF band)
- **Distance:** 400 km
- **Fading:** Rayleigh fading model
- **Noise:** Additive White Gaussian Noise (AWGN)
- **Modulation:** Simulated digital modulation

### Telemetry Data

```
Packet format:
├── Header (identifier, timestamp)
├── Position (GPS coordinates)
├── Speed and altitude
├── Battery status
└── Sensor data
```

## 🎯 Application Areas

- Testing drone communication systems
- Developing anti-jamming strategies
- Validating HF radio protocols
- Modeling military/civilian UAV communication

## Author
Zsombi & Hermes Agent (Nous Research)
