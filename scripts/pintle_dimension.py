import math

# --- INPUTS (SI UNITS) ---
wdot_fuel = 0.016        # kg/s (Liquid Isopar H)
wdot_gox = 0.034         # kg/s (Example GOX flow for O/F ~2.1)
rho_fuel = 810           # kg/s^3
rho_gox = 16.5           # kg/m^3 (At 12 bar / 20C - YOU MUST CHECK THIS)
target_tmr = 1.2         # Momentum balance target
cd_liquid = 0.7          # Discharge coeff for pintle slot/holes
cd_gas = 0.8             # Discharge coeff for annulus

# Pressure Drops (from our previous sweep)
dp_fuel_pa = 4.0 * 100000 
dp_gox_pa = 2.0 * 100000  # Usually lower for gas to keep velocity sane

# --- CALCULATIONS ---

# 1. Velocities
v_fuel = cd_liquid * math.sqrt(2 * dp_fuel_pa / rho_fuel)
v_gox = cd_gas * math.sqrt(2 * dp_gox_pa / rho_gox)

# 2. Required Areas (m^2)
area_fuel = wdot_fuel / (rho_fuel * v_fuel)
area_gox = wdot_gox / (rho_gox * v_gox)

# 3. Physical Dimensions (Assumed Pintle Diameter D_pt = 10mm for 100N engine)
d_pt_mm = 10.0
d_pt_m = d_pt_mm / 1000

# L_open (The width of the radial slot or height of holes)
# Area = PI * D_pt * L_open
l_open_m = area_fuel / (math.pi * d_pt_m)

# delta_ann (The width of the axial gas gap)
# Area = PI * D_pt * delta_ann (approx for thin gaps)
delta_ann_m = area_gox / (math.pi * d_pt_m)

print(f"--- PINTLE DIMENSIONING RESULTS ---")
print(f"Radial Fuel Velocity: {v_fuel:.2f} m/s")
print(f"Axial GOX Velocity:   {v_gox:.2f} m/s")
print(f"-----------------------------------")
print(f"Pintle Diameter (D_pt): {d_pt_mm} mm (Assumed)")
print(f"Radial Slot Width (L_open): {l_open_m*1000:.3f} mm")
print(f"Annular Gap Width (delta_ann): {delta_ann_m*1000:.3f} mm")
print(f"Skip Length (L_skip): {l_open_m*1000*2:.2f} mm (Rule: 2x L_open)")
