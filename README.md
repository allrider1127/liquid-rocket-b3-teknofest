# KOR B3 Engine Analysis Suite (TEKNOFEST 2026)

This repository contains the computational analysis tools for the **KOR (Kinetic Open Research)** liquid rocket engine, developed for the TEKNOFEST B3 competition.

## Overview
The suite is designed for a **100N GOX/Isopar-H** liquid rocket engine, optimized for the **0.9 bar** atmospheric conditions of Aksaray.

## Features
- **Propellant CEA**: Automated sweeps for Isopar-H performance.
- **Parametric Geometry**: Dynamic calculation of $D_t$, $D_e$, and $\epsilon$ based on target thrust.
- **Thermal Analysis**: Bartz-equation based gas-side heat flux estimation.
- **Dockerized Workflow**: Fully reproducible environment for engineering simulations.

## How to Use
### 1. Using Docker (Recommended)
Pull the pre-configured environment:
```bash
docker pull allrider1127/liquid-rocket-b3-teknofest:v1
```

Run the analysis:
```bash

docker compose run b3-analyzer python3 scripts/run_gox_isopar_h.py
```

## 2. Manual Installation

Ensure you have RocketCEA and math libraries installed, then run:
Bash

python3 scripts/run_gox_isopar_h.py

## Design Point Summary

   Thrust: 100N (Aksaray)

   Propellants: GOX / Isopar-H

   Chamber Pressure: 10 Bar

   Exit Pressure: 0.9 Bar
