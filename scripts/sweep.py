from rocketprops.rocket_prop import get_prop
from rocketprops.line_supt import calc_line_vel_dp
from rocketprops.valve_supt import kv_valve_dp
import math
import numpy as np

# ==========================================
# Metric Converters
# ==========================================
def c_to_r(c): return (c + 273.15) * 1.8
def bar_to_psia(bar): return bar * 14.5038
def psia_to_bar(psia): return psia / 14.5038
def kgs_to_lbms(kgs): return kgs * 2.20462
def m_to_in(m): return m * 39.3701
def mm_to_in(mm): return mm / 25.4

# ==========================================
# Engine Constants
# ==========================================
fuel = get_prop('RP1') 
T_room_R = c_to_r(20.0)

# Your Engine Targets
P_chamber_bar = 10.0
wdot_kgs = 0.016
wdot_lbms = kgs_to_lbms(wdot_kgs)

# Standard metric tubing (4mm Inner Diameter is standard for 1/4" OD tubes)
line_ID_mm = 4.0 
line_length_m = 0.5 

print("\n" + "="*85)
print(" TEKNOFEST 100N IDEAL FEED SYSTEM SWEEP (ISOPAR H)")
print("="*85)
print(f"Chamber: {P_chamber_bar} bar | Flow: {wdot_kgs} kg/s | Line: {line_ID_mm}mm ID x {line_length_m}m")
print("-" * 85)
print(f"{'Target Inj Drop':<16} | {'Valve Kv':<10} | {'REQ. FEED PRES':<16} | {'ORIFICE DIAMETER'}")
print("-" * 85)

# Test Injector Drops from 3.0 to 7.0 bar
for inj_drop_bar in [3.0, 4.0, 5.0, 6.0, 7.0]:
    
    # Calculate exact Orifice Diameter analytically (Cd = 0.7, rho = 810 kg/m^3)
    # Area = mass_flow / (Cd * sqrt(2 * density * delta_P))
    delta_P_pascals = inj_drop_bar * 100000
    area_m2 = wdot_kgs / (0.70 * math.sqrt(2 * 810 * delta_P_pascals))
    orifice_diam_mm = math.sqrt((4 * area_m2) / math.pi) * 1000
    
    # Test standard commercial valves (0.05 is restrictive, 0.20 is high flow)
    for valve_Kv in [0.05, 0.10, 0.20]:
        
        # 1. Line Pressure Drop (Assuming feed pressure is roughly Pc + Inj Drop for density calc)
        P_feed_est_psia = bar_to_psia(P_chamber_bar + inj_drop_bar)
        _, line_dp_psia = calc_line_vel_dp(
            fuel, TdegR=T_room_R, Ppsia=P_feed_est_psia,
            wdotPPS=wdot_lbms, IDinches=mm_to_in(line_ID_mm),
            roughness=5.0E-6, Kfactors=5.0, len_inches=m_to_in(line_length_m)
        )
        line_dp_bar = psia_to_bar(line_dp_psia)
        
        # 2. Valve Pressure Drop
        valve_dp_psia = kv_valve_dp(fuel, Kv=valve_Kv, wdotPPS=wdot_lbms, TdegR=T_room_R, Ppsia=P_feed_est_psia)
        valve_dp_bar = psia_to_bar(valve_dp_psia)
        
        # 3. Calculate Required Tank Pressure
        req_feed_pres = P_chamber_bar + line_dp_bar + valve_dp_bar + inj_drop_bar
        
        print(f"{inj_drop_bar:<12.1f} bar | {valve_Kv:<10.2f} | >> {req_feed_pres:<9.2f} bar << | {orifice_diam_mm:.2f} mm")
    
    print("-" * 85)
