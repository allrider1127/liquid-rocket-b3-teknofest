import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
V_tank_L = 5.0        # Total Tank Volume (Liters)
V_prop_initial_L = 3.5 # Initial Propellant Volume (Liters)
P_initial_bar = 25.0  # Starting pressure (Tank pressure)
P_chamber_bar = 10.0  # Regulated or design chamber pressure
rho_prop = 950        # Density (kg/m3) for your PG/Eth blend
mdot_initial = 0.050  # Initial mass flow rate (kg/s)
burn_time_target = 10 # Seconds
gamma = 1.4           # Adiabatic index for Pressurant (N2)

# --- SIMULATION ---
dt = 0.1
time = np.arange(0, burn_time_target, dt)
pressures = []
thrusts = []

# State variables
V_gas = (V_tank_L - V_prop_initial_L) / 1000.0 # m3
P_current = P_initial_bar * 100000.0           # Pa

for t in time:
    # 1. Store current pressure (in bar)
    pressures.append(P_current / 100000.0)
    
    # 2. Simple thrust scaling (F ~ P_tank)
    thrust = 100.0 * (P_current / (P_initial_bar * 100000.0))
    thrusts.append(thrust)
    
    # 3. Calculate how much propellant left (assume mdot scales with sqrt(dP))
    # mdot = Cd * A * sqrt(2 * rho * delta_P)
    mdot = mdot_initial * np.sqrt(max(0, (P_current/100000.0 - P_chamber_bar) / (P_initial_bar - P_chamber_bar)))
    
    # 4. Volume change
    dV = (mdot / rho_prop) * dt
    V_gas += dV
    
    # 5. Pressure change (Isentropic expansion: P1*V1^gamma = P2*V2^gamma)
    # P_new = P_old * (V_old / V_new)^gamma
    P_current = (P_initial_bar * 100000.0) * (((V_tank_L - V_prop_initial_L)/1000.0) / V_gas)**gamma

# --- PLOTTING ---
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(time, pressures, 'r', label='Tank Pressure')
plt.axhline(y=P_chamber_bar, color='k', linestyle='--', label='Chamber Press')
plt.xlabel('Time (s)'); plt.ylabel('Pressure (bar)'); plt.legend()

plt.subplot(1, 2, 2)
plt.plot(time, thrusts, 'b', label='Thrust')
plt.xlabel('Time (s)'); plt.ylabel('Thrust (N)'); plt.legend()

plt.tight_layout()
plt.savefig('/app/outputs/blowdown_results.png')
print("Simulation complete. Graph saved to outputs/blowdown_results.png")
