import sys
from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_fuel

# --- 1. ENGINE CONFIGURATION ---
Pc = 10.0 # Chamber Pressure in bar
Pamb = 0.9 # Ambient Exhaust Pressure in bar

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

Pc_over_Pe = Pc / Pamb

print("\nRunning Thermo-Chemical Matrix Sweep (100% Ethanol -> 100% Propylene Glycol)...")
print("="*120)
header = f"| {'Eth% / PG%':<11} | {'Mol Frac Eth':<12} | {'Mol Frac PG':<11} | {'Flam Index(100F)':<16} | {'Flash Pt > 100F?':<18} | {'Opt O/F':<7} | {'Opt Vac Isp':<11} | {'Opt Amb Isp':<11} |"
print(header)
print("|" + "-"*13 + "|" + "-"*14 + "|" + "-"*13 + "|" + "-"*18 + "|" + "-"*20 + "|" + "-"*9 + "|" + "-"*13 + "|" + "-"*13 + "|")

for pg_pct in range(0, 101, 5):
    eth_pct = 100 - pg_pct
    
    # Calculate Liquid Mole Fractions
    m_eth = eth_pct / MW_eth
    m_pg = pg_pct / MW_pg
    total_m = m_eth + m_pg
    
    if total_m == 0: continue
        
    x_eth = m_eth / total_m
    x_pg = m_pg / total_m
    
    # Calculate Partial Pressures and Vapor Mole Fractions (Raoult's Law)
    y_eth = (x_eth * P_eth_star_bar) / P_atm_bar
    y_pg = (x_pg * P_pg_star_bar) / P_atm_bar
    
    # Flammability Index
    flam_index = (y_eth / LFL_eth) + (y_pg / LFL_pg)
    is_safe = "✅ Yes (Safe)" if flam_index < 1.0 else "❌ No (Flashes)"
    
    # Define Fuel for CEA
    fuel_name = f"Matrix_Blend_{eth_pct}_{pg_pct}"
    custom_fuel_card = f"""
    fuel Ethanol         C 2.0 H 6.0 O 1.0  wt%={eth_pct:.1f}  h,cal=-66370.0   t(k)=298.15  rho=0.789
    fuel PropGlycol      C 3.0 H 8.0 O 2.0  wt%={pg_pct:.1f}  h,cal=-115153.0  t(k)=298.15  rho=1.036
    """
    
    try: add_new_fuel(fuel_name, custom_fuel_card)
    except Exception: pass
        
    C = CEA_Obj( oxName='GOX', fuelName=fuel_name, 
                 pressure_units='bar', cstar_units='m/s', 
                 temperature_units='K', isp_units='sec',
                 density_units='kg/m^3', specific_heat_units='J/kg-K')
                 
    best_IspVac = 0
    best_IspAmb = 0
    best_MR = 0
    
    # Sweep O/F to find peak Vacuum Isp
    for mr_int in range(10, 31, 1):
        mr = mr_int / 10.0
        try:
            eps = C.get_eps_at_PcOvPe(Pc=Pc, MR=mr, PcOvPe=Pc_over_Pe)
            if eps is None or eps <= 1.0: continue
            
            IspVac, Cstar, Tc, mw, gam = C.get_IvacCstrTc_ChmMwGam(Pc=Pc, MR=mr, eps=eps)
            IspAmb, mode = C.estimate_Ambient_Isp(Pc=Pc, MR=mr, eps=eps, Pamb=Pamb)
            
            if IspVac > best_IspVac:
                best_IspVac = IspVac
                best_IspAmb = IspAmb
                best_MR = mr
        except Exception:
            continue
            
    blend_label = f"{eth_pct}% / {pg_pct}%"
    print(f"| {blend_label:<11} | {x_eth:<12.3f} | {x_pg:<11.3f} | {flam_index:<16.3f} | {is_safe:<18} | {best_MR:<7.1f} | {best_IspVac:<11.2f} | {best_IspAmb:<11.2f} |")

print("="*120)
