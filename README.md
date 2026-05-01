## KOR B3 Engine Analysis Suite (TEKNOFEST 2026)

This repository contains the integrated computational analysis tools for the KOR (Kinetic Open Research) liquid rocket engine. 
Developed specifically for the TEKNOFEST B3 competition, the suite provides a "Digital Twin" for a 100N GOX/Isopar-H liquid engine.

## Overview

The suite is optimized for the 0.9 bar atmospheric conditions of Aksaray, ensuring optimal nozzle expansion and performance at the competition site.
Features

    Integrated Propellant CEA: Automated sweeps for Isopar-H/GOX performance at specific mixture ratios.

    Dynamic Geometry: Calculation of Dt​, De​, and ϵ based on a 100N thrust target.

    Thermal Analysis: Bartz-equation based gas-side heat flux estimation to verify the integrity of the 100mm copper block.

    Transient Priming Simulation: Calculates propellant travel times to ensure a Safe Oxidizer Lead.

    Mechanical Safety Verification: Tie-rod structural analysis for the modular engine stack, ensuring high safety factors for high-pressure testing.

    Dockerized Workflow: Fully reproducible environment for engineering simulations.

# How to Use
## 1. Using Docker (Recommended)

Pull the pre-configured environment containing the latest solver and integrated scripts:
```Bash

docker pull allrider1127/liquid-rocket-b3-teknofest:latest

```

Run the Master Performance Summary:
```Bash

docker run -it allrider1127/liquid-rocket-b3-teknofest:latest python3 scripts/polvon_b3_master.py
```

## 2. Core Scripts

    run_gox_isopar_h.py: Core internal ballistics and CEA sweep.

    injector_priming.py: Start-up transient and priming delay analysis.

    polvon_b3_master.py: Generates the Master Performance Summary Table for the technical report.

    bolt_analysis.py: Structural safety verification for the tie-rod assembly.

Design Point Summary

    Thrust: 100N (Aksaray Ambient)

    Propellants: GOX / Isopar-H

    Chamber Pressure: 10 Bar

    Exit Pressure: 0.9 Bar

    Optimal O/F: 2.2
