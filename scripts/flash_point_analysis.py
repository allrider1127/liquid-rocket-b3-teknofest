import sys
from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_fuel

# --- 1. ENGINE CONFIGURATION ---
Pc = 10.0 # Chamber Pressure in bar
Pamb = 0.9 # Ambient Exhaust Pressure in bar
thrust_target = 100.0 # Target Thrust in Newtons
g0 = 9.80665 # Standard gravity in m/s^2

# --- 2. VAPOR PRESSURE & FLASH POINT CONSTANTS AT 100 F (310.93 K) ---
T_K = 310.93
P_atm_bar = 1.01325

# Antoine Coefficients (P in bar, T in K) and LFLs
# Ethanol (C2H6O)
A_eth = 5.24677; B_eth = 1598.673; C_eth = -46.424
P_eth_star_bar = 10 ** (A_eth - B_eth / (T_K + C_eth))
LFL_eth = 0.033 # 3.3% Lower Flammability Limit
MW_eth = 46.07

# Propylene Glycol (C3H8O2)
A_pg = 6.07936; B_pg = 2692.187; C_pg = -17.94
P_pg_star_bar = 10 ** (A_pg - B_pg / (T_K + C_pg))
LFL_pg = 0.026 # 2.6% Lower Flammability Limit
MW_pg = 76.09

print("="*105)
print("Flash Point and Performance Optimization Analysis")
print("Target: Find minimum Propylene Glycol % that keeps Flash Point > 100 F & Vacuum Isp > 260 s")
print("="*105)

Pc_over_Pe = Pc / Pamb

for pg_pct in range(0, 101):
    eth_pct = 100 - pg_pct
    
    # Calculate Mole Fractions in Liquid Phase
    m_eth = eth_pct / MW_eth
    m_pg = pg_pct / MW_pg
    total_m = m_eth + m_pg
    
    if total_m == 0:
        continue
        
    x_eth = m_eth / total_m
    x_pg = m_pg / total_m
    
    # Calculate Partial Pressures and Vapor Mole Fractions (Raoult's Law)
    y_eth = (x_eth * P_eth_star_bar) / P_atm_bar
    y_pg = (x_pg * P_pg_star_bar) / P_atm_bar
    
    # Flammability Index (Le Chatelier's mixing rule)
    flam_index = (y_eth / LFL_eth) + (y_pg / LFL_pg)
    
    # If flam_index >= 1.0, the mixture vapor flashes at 100F. 
    if flam_index >= 1.0:
        continue # Not safe, try next percentage (meaning add more PG)
        
    # If we reached here, Flash Point is > 100 F (Meaning it's SAFE)
    
    # Set up RocketCEA to check Vacuum Isp
    fuel_name = f"Flash_Blend_{eth_pct}_{pg_pct}"
    custom_fuel_card = f"""
    fuel Ethanol         C 2.0 H 6.0 O 1.0  wt%={eth_pct:.1f}  h,cal=-66370.0   t(k)=298.15  rho=0.789
    fuel PropGlycol      C 3.0 H 8.0 O 2.0  wt%={pg_pct:.1f}  h,cal=-115153.0  t(k)=298.15  rho=1.036
    """
    
    try:
        add_new_fuel(fuel_name, custom_fuel_card)
    except Exception:
        pass
        
    C = CEA_Obj( oxName='GOX', fuelName=fuel_name, 
                 pressure_units='bar', cstar_units='m/s', 
                 temperature_units='K', isp_units='sec',
                 density_units='kg/m^3', specific_heat_units='J/kg-K')
                 
    best_IspVac = 0
    best_MR = 0
    
    # Sweep O/F to find the maximum Vacuum Isp for this specific blend
    for mr_int in range(10, 36, 1):
        mr = mr_int / 10.0
        try:
            eps = C.get_eps_at_PcOvPe(Pc=Pc, MR=mr, PcOvPe=Pc_over_Pe)
            if eps is None or eps <= 1.0: continue
            IspVac, Cstar, Tc, mw, gam = C.get_IvacCstrTc_ChmMwGam(Pc=Pc, MR=mr, eps=eps)
            if IspVac > best_IspVac:
                best_IspVac = IspVac
                best_MR = mr
        except Exception:
            continue
            
    if best_IspVac >= 260.0:
        print(f"** SUCCESS! Perfect safe blend found:")
        print(f"-> Propylene Glycol (% by weight): {pg_pct}%")
        print(f"-> Ethanol (% by weight): {eth_pct}%")
        print(f"Flash Point Condition: Safe (Flammability Index at 100F = {flam_index:.3f} < 1.0)")
        print(f"Max Vacuum Specific Impulse: {best_IspVac:.2f} s (at Optimum O/F = {best_MR})")
        break
    else:
        # If the highest allowed ethanol doesn't reach 260s, no safe mixture will.
        print(f"** ANALYSIS COMPLETE: ")
        print(f"The safest minimum boundary is {pg_pct}% PG / {eth_pct}% Ethanol (Index {flam_index:.3f}).")
        print(f"However, the max Vacuum Isp for this blend drops to {best_IspVac:.2f} s (at O/F {best_MR}).")
        print(f"It is mathematically IMPOSSIBLE to meet >260s IspVac while keeping Flash Point > 100F under these conditions.")
        break
