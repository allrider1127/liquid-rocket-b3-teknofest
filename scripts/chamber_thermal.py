kimport math
# Importing results from your CEA sweep
from run_gox_isopar_h import C, best_MR_vac, Pc, At_cm2 

# --- AUTOMATIC DATA EXTRACTION ---
mr = best_MR_vac 

# Extracting live performance data for the optimum Mixture Ratio
# We use a fixed expansion ratio of 2.5 for the thermal check
IspVac, Cstar_ms, Tc_K, mw, gamma = C.get_IvacCstrTc_ChmMwGam(Pc=Pc, MR=mr, eps=2.5)

# --- CALCULATING DIAMETER FROM AREA ---
# At_cm2 is the area in cm^2 from your CEA results
Dt_cm = 2 * math.sqrt(At_cm2 / math.pi)
Dt_m = Dt_cm / 100  # Convert to meters

# --- PHYSICAL CONSTANTS (Gas Properties at Throat) ---
Pr = 0.71            # Prandtl number
mu = 0.88e-4         # Viscosity (kg/m-s)
Cp = 2300            # Specific heat (J/kg-K)

# --- BARTZ EQUATION ---
# hg = [0.026 / Dt^0.2] * [mu^0.2 * Cp / Pr^0.6] * (Pc_pa / Cstar)^0.8
Pc_pa = Pc * 1e5
hg = (0.026 / (Dt_m**0.2)) * (mu**0.2 * Cp / (Pr**0.6)) * (Pc_pa / Cstar_ms)**0.8

# --- HEAT FLUX CALCULATION ---
Tw = 800  # Assumed inner wall temp in Kelvin
q = hg * (Tc_K - Tw)

print(f"--- KOR B3 INTEGRATED THERMAL RESULTS ---")
print(f"Fuel: Isopar-H | Optimum MR: {mr}")
print(f"Combustion Temp (Tc): {Tc_K:.2f} K")
print(f"C-Star: {Cstar_ms:.2f} m/s")
print(f"Throat Diameter (Dt): {Dt_cm:.3f} cm")
print(f"Gas-side hg: {hg:.2f} W/m^2-K")
print(f"Throat Heat Flux (q): {q/1e6:.2f} MW/m^2")
