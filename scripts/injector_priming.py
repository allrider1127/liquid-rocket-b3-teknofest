import numpy as np
import math
from run_gox_isopar_h import mdot_f, mdot_ox # Pulling live 100N flows

def calculate_priming():
    print(f"{'--- PARAMETRIC FEED SYSTEM ANALYSIS ---':^50}")
    
    # --- USER INPUTS ---
    try:
        L_pipe = float(input("Enter total feed line length from valve to engine (meters): "))
        D_pipe_mm = float(input("Enter feed line internal diameter (mm) [Suggested ~2.4]: "))
        L_regen = float(input("Enter estimated length of Regen cooling path (meters) [0 if none]: "))
        D_regen_mm = float(input("Enter Regen tube internal diameter (mm): "))
    except ValueError:
        print("Invalid input. Using default design specs.")
        L_pipe, D_pipe_mm, L_regen, D_regen_mm = 0.5, 2.36, 0.2, 2.0

    # --- GEOMETRY CALCULATIONS ---
    area_pipe = math.pi * ((D_pipe_mm / 1000) / 2)**2
    area_regen = math.pi * ((D_regen_mm / 1000) / 2)**2
    
    vol_pipe = area_pipe * L_pipe
    vol_regen = area_regen * L_regen
    vol_manifold = 5.0e-7 # Existing 50mm copper block plenum volume
    
    total_fuel_vol = vol_pipe + vol_regen + vol_manifold
    
    # --- FLUID PHYSICS ---
    rho_fuel = 800.0  # Isopar-H
    rho_ox = 1.429    # GOX (simplified for priming front)
    
    Q_f = mdot_f / rho_fuel
    Q_ox = mdot_ox / rho_ox
    
    # --- TIMING RESULTS ---
    tau_f = (total_fuel_vol / Q_f) * 1000 # Convert to ms
    tau_ox = (vol_manifold / Q_ox) * 1000 # GOX manifold only for now
    
    print("\n" + "="*50)
    print(f"Total Fuel System Volume: {total_fuel_vol*1e6:.2f} cm^3")
    print(f"Fuel Priming Delay (Total): {tau_f:.2f} ms")
    print(f"Oxidizer Priming Delay:      {tau_ox:.2f} ms")
    print(f"Start-up Lead/Lag:           {tau_f - tau_ox:.2f} ms (Fuel Lag)")
    print("="*50)
    
    if (tau_f - tau_ox) > 50:
        print("WARNING: High Fuel Lag detected. Consider shorter lines to avoid ignition timeout.")
    elif (tau_f - tau_ox) < 0:
        print("CRITICAL WARNING: Fuel Lead detected! Risk of Hard Start (explosion).")
    else:
        print("STATUS: Safe Oxidizer Lead established.")

if __name__ == "__main__":
    calculate_priming()
def get_results():
    # Geometry for default calculation if imported
    L_pipe, D_pipe_mm, L_regen, D_regen_mm = 0.5, 2.36, 0.2, 2.0
    
    vol_pipe = (math.pi * ((D_pipe_mm / 1000) / 2)**2) * L_pipe
    vol_regen = (math.pi * ((D_regen_mm / 1000) / 2)**2) * L_regen
    vol_manifold = 5.0e-7
    
    rho_fuel, rho_ox = 800.0, 1.429
    
    t_f = ((vol_pipe + vol_regen + vol_manifold) / (mdot_f / rho_fuel)) * 1000
    t_ox = (vol_manifold / (mdot_ox / rho_ox)) * 1000
    return t_f, t_ox

# This handles both running the script standalone and importing it
if __name__ == "__main__":
    calculate_priming()
    # Create global vars for master script to see
    tau_f, tau_ox = get_results()
else:
    # If imported by master script, use default design values
    tau_f, tau_ox = get_results()
