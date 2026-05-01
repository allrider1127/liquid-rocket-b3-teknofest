import sys
import math
from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_fuel

# --- 1. DEFINE CUSTOM FUEL ---
# Isopar-H is highly refined isoparaffinic hydrocarbon 
# Approximate properties: C12H26, Hf ~ -65,000 cal/mol, rho = 0.76 g/cc
custom_fuel_card = """
fuel IsoparH  C 12.0 H 26.0  wt%=100.0  h,cal=-65000.0  t(k)=298.15  rho=0.76
"""
add_new_fuel('IsoparH', custom_fuel_card)

# --- ENGINE CONFIGURATION ---
Pc = 10.0 # Chamber Pressure in bar
Pamb = 0.9 # Ambient Exhaust Pressure in bar
thrust_target = 100.0 # Target Thrust in Newtons
g0 = 9.80665 # Standard gravity in m/s^2

# --- INITIALIZE ROCKETCEA ---
C = CEA_Obj( oxName='GOX', fuelName='IsoparH', 
             pressure_units='bar', 
             cstar_units='m/s', 
             temperature_units='K', 
             isp_units='sec',
             density_units='kg/m^3',
             specific_heat_units='J/kg-K')
#
print("="*105)
print(f"RocketCEA Case: Thrust = {thrust_target} N, Pc = {Pc} bar, Pamb = {Pamb} bar")
print("Propellants: Gaseous Oxygen (GOX) / Isopar-H")
print("Expansion to Ambient Pressure (Optimal Pexit = Pamb)")
print("="*105)
print(f"{'O/F(MR)':<8} {'Isp_amb(s)':<12} {'Isp_vac(s)':<12} {'Gamma(y)':<10} {'Tc(K)':<8} {'eps(A_e/A_t)':<12} {'mdot(kg/s)':<12} {'At(cm^2)':<10} {'Ae(cm^2)':<10}")
print("-" * 105)

Pc_over_Pe = Pc / Pamb

best_MR_vac = 0
best_IspVac = 0
best_MR_amb = 0
best_IspAmb = 0
best_Dt_cm = 0
best_De_cm = 0
best_At_cm2 = 0
best_Ae_cm2 = 0
best_Tc = 0
best_Cstar = 0
best_gamma = 0

# Loop O/F Mixture ratios from 1.5 -> 3.5 in increments of 0.1
for mr_int in range(15, 36, 1):
    mr = mr_int / 10.0
    
    # 1. Get the ideal area expansion ratio (eps) for our pressure ratio
    try:
        eps = C.get_eps_at_PcOvPe(Pc=Pc, MR=mr, PcOvPe=Pc_over_Pe)
    except Exception:
        continue # skip failure points if mixture ratio is unsustainable
        
    if eps is None or eps <= 1.0:
        continue
        
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
    Dt_cm = 2 * math.sqrt(At_cm2 / math.pi)
    Rt_cm = Dt_cm / 2
    De_cm = 2 * math.sqrt(Ae_cm2 / math.pi)
    Re_cm = De_cm / 2


    # Track maximums
    if IspVac > best_IspVac:
        best_IspVac = IspVac
        best_MR_vac = mr
        
    if IspAmb > best_IspAmb:
        best_IspAmb = IspAmb
        best_MR_amb = mr
        best_Dt_cm = Dt_cm
        best_De_cm = De_cm
        best_At_cm2 = At_cm2
        best_Ae_cm2 = Ae_cm2
        best_Tc = Tc
        best_Cstar = Cstar
        best_gamma = gam


        
    print(f"{mr:<8.1f} {IspAmb:<12.2f} {IspVac:<12.2f} {gam:<10.4f} {Tc:<8.1f} {eps:<12.3f} {mdot:<12.4f} {At_cm2:<10.3f} {Ae_cm2:<10.3f}")

print("="*105)
print(f"** Optimum O/F based on Vacuum Isp: {best_MR_vac:.1f} (Isp_vac = {best_IspVac:.2f} s)")
print(f"** Optimum O/F based on Ambient Isp: {best_MR_amb:.1f} (Isp_amb = {best_IspAmb:.2f} s)")
# =============================================================================
# TEKNOFEST B3 - FINAL ENGINE DIMENSIONING (REGULATED 10 BAR CASE)
# =============================================================================
print("\n" + "="*60)
print(f"{'ENGINE GEOMETRY & PERFORMANCE SUMMARY':^60}")
print("="*60)

# Performance Data at Optimum
print(f"{'--- Performance Stats ---':<30}")
print(f"Optimum O/F Ratio:          {best_MR_vac:.2f}")
print(f"Chamber Temperature (Tc):   {best_Tc:.2f} K")
print(f"Vacuum Isp:                 {best_IspVac:.2f} s")
print(f"Ambient Isp:                {best_IspAmb:.2f} s")
print(f"Characteristic Vel (C*):    {best_Cstar:.2f} m/s")
print(f"Adiabatic Index (Gamma):    {best_gamma:.4f}")

print(f"\n{'--- Nozzle Dimensions ---':<30}")
print(f"Throat Area (At):           {best_At_cm2:.4f} cm^2")
print(f"Throat Diameter (Dt):       {best_Dt_cm:.4f} cm")
print(f"Throat Radius (Rt):         {best_Dt_cm/2.0:.4f} cm")
print(f"Exit Area (Ae):             {best_Ae_cm2:.4f} cm^2")
print(f"Exit Diameter (De):         {best_De_cm:.4f} cm")
print(f"Exit Radius (Re):           {best_De_cm/2.0:.4f} cm")
print(f"Expansion Ratio (Eps):      {best_Ae_cm2/best_At_cm2:.3f}")

print(f"\n{'--- Mass Flow (Total) ---':<30}")
# Total mdot calculation
mdot_total = thrust_target / (best_IspAmb * g0)
# Individual flow rates: 
# mdot_total = mdot_f + mdot_ox  AND  mdot_ox = best_MR_amb * mdot_f
# Therefore: mdot_f = mdot_total / (1 + best_MR_amb)
mdot_f = mdot_total / (1 + best_MR_amb)
mdot_ox = mdot_total - mdot_f

print(f"Total Mass Flow (mdot):     {mdot_total:.5f} kg/s")
print(f"GOX Mass Flow (mdot_ox):    {mdot_ox:.5f} kg/s")
print(f"Isopar-H Flow (mdot_f):     {mdot_f:.5f} kg/s")
print(f"Target O/F Ratio:           {best_MR_amb:.2f}")
print("="*60)
