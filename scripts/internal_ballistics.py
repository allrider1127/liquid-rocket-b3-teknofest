import numpy as np
import matplotlib.pyplot as plt
import math
# Pulling live data from your main source
from run_gox_isopar_h import C, best_MR_amb, Pc, At_cm2

# --- 1. LIVE DATA EXTRACTION ---
# We use the MR optimized for Aksaray (2.2)
mr = best_MR_amb 
IspVac, Cstar_ms, Tc_K, mw, gamma = C.get_IvacCstrTc_ChmMwGam(Pc=Pc, MR=mr, eps=2.5)

# Convert units for the simulation
At_m2 = At_cm2 / 10000.0  # cm^2 to m^2
Pc_steady_pa = Pc * 100000.0  # bar to Pa
L_star = 1.0  # From your RPA design
Vc = L_star * At_m2
R_spec = 8314.0 / mw  # Specific gas constant based on molar mass from CEA

# --- 2. TRANSIENT SIMULATION LOGIC ---
dt = 0.00001  # 0.01ms steps for higher resolution
t_end = 0.05
time = np.arange(0, t_end, dt)
Pc_array = np.zeros_like(time)
Thrust_array = np.zeros_like(time)

# Starting at ambient pressure (Aksaray 0.9 bar)
Pc_array[0] = 0.9 * 101325 
mdot_in = (Pc_steady_pa * At_m2) / Cstar_ms

tau_valve = 0.020 # 20ms valve opening ramp

for i in range(1, len(time)):
    # Model the valve opening gradually
    valve_factor = min(time[i] / tau_valve, 1.0)
    current_mdot_in = mdot_in * valve_factor
    
    mdot_out = (Pc_array[i-1] * At_m2) / Cstar_ms
    dPc_dt = (R_spec * Tc_K / Vc) * (current_mdot_in - mdot_out)
    
    Pc_array[i] = Pc_array[i-1] + dPc_dt * dt
    Thrust_array[i] = 1.35 * Pc_array[i] * At_m2
    
    # Calculate Thrust (Simplified Cf for the ramp-up)
    # At steady state, this will reach your 100N target
    Thrust_array[i] = 1.35 * Pc_array[i] * At_m2

# --- 3. PLOTTING ---
plt.figure(figsize=(12, 5))

# Pressure Plot
plt.subplot(1, 2, 1)
plt.plot(time, Pc_array / 1e5, color='red', linewidth=2)
plt.axhline(y=Pc, color='black', linestyle='--', label='Steady State (10 bar)')
plt.title('Basınç-Zaman Simülasyonu (Pressure-Time)')
plt.xlabel('Zaman (s)')
plt.ylabel('Basınç (bar)')
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()

# Thrust Plot
plt.subplot(1, 2, 2)
plt.plot(time, Thrust_array, color='blue', linewidth=2)
plt.axhline(y=100, color='black', linestyle='--', label='Target Thrust (100N)')
plt.title('İtki-Zaman Simülasyonu (Thrust-Time)')
plt.xlabel('Zaman (s)')
plt.ylabel('İtki (N)')
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()

plt.tight_layout()
plt.savefig('/app/outputs/internal_ballistics_live.png')
print(f"Success: Simulation synced with run_gox_isopar_h.py at MR={mr}")
