# drone-radio-simulator

HF band (2-5 MHz) drone radio communication and interference simulator.

## Overview & Purpose
drone-radio-simulator models high-frequency radio signal attenuation, telemetry protocol packet delivery, and jamming resistance between unmanned aerial vehicles and ground control stations.

## Key Features
- HF radio propagation loss modeling (2-5 MHz).
- Telemetry packet transmission simulation.
- Jamming signal power ratio analysis.

## Tech Stack & Dependencies
- **Language**: Python 3.9+
- **Libraries**: NumPy, SciPy, Matplotlib

## Project Structure
```text
drone-radio-simulator/
├── simulator.py
├── radio_model.py
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.9+

### Steps
```bash
git clone https://github.com/zsomborturcsanyi7-lang/drone-radio-simulator.git
cd drone-radio-simulator
pip install numpy scipy matplotlib
python simulator.py
```

## Usage Examples
```bash
python simulator.py --freq 3.5 --power 10
```

## Status & License
Status: Simulation Prototype.
License: MIT
