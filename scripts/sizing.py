from rocketprops.rocket_prop import get_prop
from rocketprops.line_supt import calc_line_id_dp
from rocketprops.valve_supt import kv_valve_dp  # Switched to metric Kv
from rocketprops.injector_supt import calc_orifice_flow_rate
import numpy as np

# ==========================================
# SI <-> Imperial Conversion Helpers
# ==========================================
def c_to_r(c): return (c + 273.15) * 1.8
def bar_to_psia(bar): return bar * 14.5038
def psia_to_bar(psia): return psia / 14.5038
def kgs_to_lbms(kgs): return kgs * 2.20462
def lbms_to_kgs(lbms): return lbms / 2.20462
def ms_to_fps(ms): return ms * 3.28084
def m_to_in(m): return m * 39.3701
def in_to_mm(inches): return inches * 25.4
def mm_to_in(mm): return mm / 25.4

# ==========================================
# 1. Setup Propellant and SI Inputs
# ==========================================
fuel = get_prop('RP1') 

T_room_C = 20.0               # Temperature in Celsius
P_feed_bar = 12.5             # Upstream feed pressure in bar
P_chamber_bar = 10.0          # Chamber pressure in bar
wdot_fuel_kgs = 0.016         # Mass flow rate in kg/s (Example: ~16 g/s)

# Convert to Imperial for RocketProps to use internally
T_room_R = c_to_r(T_room_C)
P_feed_psia = bar_to_psia(P_feed_bar)
wdot_fuel_lbms = kgs_to_lbms(wdot_fuel_kgs)

print("\n--- ISOPAR H (RP-1) FEED SYSTEM SIZING (SI UNITS) ---")

# ==========================================
# 2. Feed Line Sizing
# ==========================================
target_velocity_ms = 4.5      # Fluid velocity in m/s
line_length_m = 0.5           # Line length in meters

line_ID_in, line_dp_psia = calc_line_id_dp(
    fuel, TdegR=T_room_R, Ppsia=P_feed_psia,
    wdotPPS=wdot_fuel_lbms, velFPS=ms_to_fps(target_velocity_ms),
    roughness=5.0E-6, Kfactors=5.0, len_inches=m_to_in(line_length_m)
)

print(f"Feed Line ID: {in_to_mm(line_ID_in):.2f} mm")
print(f"Feed Line Pressure Drop: {psia_to_bar(line_dp_psia):.3f} bar")

# ==========================================
# 3. Valve Sizing
# ==========================================
# Metric valve flow coefficient (Kv) is standard in Europe/SI
valve_Kv = 0.04 

valve_dp_psia = kv_valve_dp(fuel, Kv=valve_Kv, wdotPPS=wdot_fuel_lbms, TdegR=T_room_R, Ppsia=P_feed_psia)
print(f"Valve Pressure Drop (Kv={valve_Kv}): {psia_to_bar(valve_dp_psia):.3f} bar")

# ==========================================
# 4. Injector Orifice Sizing
# ==========================================
injector_dp_bar = 2.0  # Desired injector pressure drop in bar (e.g., 20% of 10 bar Pc)
Cd_orifice = 0.70      # Discharge coefficient

print(f"\nTarget Fuel Mass Flow: {wdot_fuel_kgs:.4f} kg/s")
print("Iterating to find correct injector orifice diameter...")

# Test diameters from 0.5 mm to 4.0 mm, stepping by 0.01 mm
for d_mm in np.arange(0.5, 4.0, 0.01):
    d_in = mm_to_in(d_mm)
    flow_lbms = calc_orifice_flow_rate(
        fuel, CdOrf=Cd_orifice, DiamInches=d_in,
        dPpsia=bar_to_psia(injector_dp_bar), TdegR=T_room_R, Ppsia=P_feed_psia
    )
    flow_kgs = lbms_to_kgs(flow_lbms)
    
    if flow_kgs >= wdot_fuel_kgs:
        print(f"--> Required Injector Orifice Diameter: ~{d_mm:.2f} mm (Produces {flow_kgs:.4f} kg/s)\n")
        break
