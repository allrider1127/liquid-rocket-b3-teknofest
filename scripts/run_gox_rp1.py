import sys
import math
from rocketcea.cea_obj_w_units import CEA_Obj

# --- ENGINE CONFIGURATION ---
Pc = 10.0 # Chamber Pressure in bar
Pamb = 0.9 # Ambient Exhaust Pressure in bar
thrust_target = 100.0 # Target Thrust in Newtons
g0 = 9.80665 # Standard gravity in m/s^2

# --- INITIALIZE ROCKETCEA ---
C = CEA_Obj( oxName='GOX', fuelName='RP1', 
             pressure_units='bar', 
             cstar_units='m/s', 
             temperature_units='K', 
             isp_units='sec',
             density_units='kg/m^3',
             specific_heat_units='J/kg-K')

print("="*105)
print(f"RocketCEA Case: Thrust = {thrust_target} N, Pc = {Pc} bar, Pamb = {Pamb} bar")
print("Propellants: Gaseous Oxygen (GOX) / RP-1 Kerosene")
print("Expansion to Ambient Pressure (Optimal Pexit = Pamb)")
print("="*105)
print(f"{'O/F(MR)':<8} {'Isp_amb(s)':<12} {'Isp_vac(s)':<12} {'Gamma(y)':<10} {'Tc(K)':<8} {'eps(A_e/A_t)':<12} {'mdot(kg/s)':<12} {'At(cm^2)':<10} {'Ae(cm^2)':<10}")
print("-" * 105)

Pc_over_Pe = Pc / Pamb

best_MR_vac = 0
best_IspVac = 0
best_MR_amb = 0
best_IspAmb = 0

# Loop O/F Mixture ratios from 1.5 -> 3.5 in increments of 0.1
for mr_int in range(15, 36, 1):
    mr = mr_int / 10.0
    
    # 1. Get the ideal area expansion ratio (eps) for our pressure ratio
    eps = C.get_eps_at_PcOvPe(Pc=Pc, MR=mr, PcOvPe=Pc_over_Pe)
        
    # 2. Extract standard properties from CEA solver
    IspAmb, mode = C.estimate_Ambient_Isp(Pc=Pc, MR=mr, eps=eps, Pamb=Pamb)
    
    # Use the ChmMwGam function to get Chamber Molecular Weight and Gamma
    IspVac, Cstar, Tc, mw, gam = C.get_IvacCstrTc_ChmMwGam(Pc=Pc, MR=mr, eps=eps)
    
    # 3. Calculate Geometry based on thrust requirement (Ambient conditions)
    mdot = thrust_target / (IspAmb * g0) # kg/s

    Pc_Pa = Pc * 100000.0                         # bar to Pascal
    At_m2 = (Cstar * mdot) / Pc_Pa                # C* = (Pt * At) / mdot
    At_cm2 = At_m2 * 10000.0                      # convert to cm^2
    Ae_cm2 = At_cm2 * eps                         # exit area

    # Track maximums
    if IspVac > best_IspVac:
        best_IspVac = IspVac
        best_MR_vac = mr
        
    if IspAmb > best_IspAmb:
        best_IspAmb = IspAmb
        best_MR_amb = mr
        
    print(f"{mr:<8.1f} {IspAmb:<12.2f} {IspVac:<12.2f} {gam:<10.4f} {Tc:<8.1f} {eps:<12.3f} {mdot:<12.4f} {At_cm2:<10.3f} {Ae_cm2:<10.3f}")

print("="*105)
print(f"** Optimum O/F based on Vacuum Isp: {best_MR_vac:.1f} (Isp_vac = {best_IspVac:.2f} s)")
print(f"** Optimum O/F based on Ambient Isp: {best_MR_amb:.1f} (Isp_amb = {best_IspAmb:.2f} s)")
