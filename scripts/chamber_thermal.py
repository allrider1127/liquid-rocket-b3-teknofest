import math
from run_gox_isopar_h import C, best_MR_amb, Pc, At_cm2

# --- 1. LIVE DATA EXTRACTION ---
mr = best_MR_amb
# Use the live results from your CEA sweep
IspVac, Cstar_ms, Tc_K, mw, gamma = C.get_IvacCstrTc_ChmMwGam(Pc=Pc, MR=mr, eps=2.5)

Dt_m = (2 * math.sqrt(At_cm2 / math.pi)) / 100  # Throat diameter in meters
R_inner = Dt_m / 2

# --- 2. GAS PROPERTIES & BARTZ ---
Pr = 0.71
mu = 0.88e-4
Cp = 2300
Pc_pa = Pc * 1e5
# Full Bartz Equation
hg = (0.026 / (Dt_m**0.2)) * (mu**0.2 * Cp / (Pr**0.6)) * (Pc_pa / Cstar_ms)**0.8

# --- 3. THE COPPER BLOCK PHYSICS ---
k_cu = 390.0        # OFHC Copper conductivity
D_outer = 0.100     # Your 100mm block
R_outer = D_outer / 2
T_aw = Tc_K * 0.98   # Adiabatic wall temperature
T_coolant = 300.0   # Bulk Isopar-H temp

# Thermal Resistance logic for a cylinder:
# We solve for Tw_inner by equating gas-side convection and wall conduction
# q = hg * (T_aw - Tw_inner) = k_cu * (Tw_inner - Tw_outer) / (R_inner * ln(R_outer/R_inner))
res_wall = (R_inner * math.log(R_outer / R_inner)) / k_cu
Tw_inner = (hg * T_aw + (1/res_wall) * T_coolant) / (hg + (1/res_wall))
q = hg * (T_aw - Tw_inner)
Tw_outer = Tw_inner - (q * res_wall)

# --- 4. OUTPUTS ---
print(f"{'--- KOR B3 INTEGRATED THERMAL RESULTS ---':^50}")
print(f"Propellants: GOX/Isopar-H | MR: {mr}")
print(f"Chamber Temp (Tc): {Tc_K:.1f} K")
print(f"Gas-side hg:       {hg:.2f} W/m^2-K")
print(f"Peak Heat Flux:    {q/1e6:.2f} MW/m^2")
print("-" * 50)
print(f"Inner Wall Temp:   {Tw_inner:.1f} K")
print(f"Outer Wall Temp:   {Tw_outer:.1f} K")
print("-" * 50)

if Tw_inner < 1000:
    print("STATUS: SUCCESS - OFHC Copper structural integrity maintained.")
if Tw_outer < 550:
    print("STATUS: SUCCESS - Silver brazing / Regen channels safe.")
