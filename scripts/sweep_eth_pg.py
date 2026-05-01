import sys
import math
from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_fuel

# --- ENGINE CONFIGURATION ---
Pc = 10.0 # Chamber Pressure in bar
Pamb = 0.9 # Ambient Exhaust Pressure in bar
thrust_target = 100.0 # Target Thrust in Newtons
g0 = 9.80665 # Standard gravity in m/s^2

print("="*115)
print(f"RocketCEA Sweep: Thrust = {thrust_target} N, Pc = {Pc} bar, Pamb = {Pamb} bar")
print("Propellants: GOX / (Ethanol + Propylene Glycol Mix)")
print("="*115)
print(f"{'Blend(Eth/PG)':<15} {'O/F(MR)':<8} {'Isp_amb(s)':<12} {'Isp_vac(s)':<12} {'Gamma(y)':<10} {'Tc(K)':<8} {'eps':<8} {'mdot(kg/s)':<12} {'At(cm^2)':<10} {'Ae(cm^2)':<10}")
print("-" * 115)

Pc_over_Pe = Pc / Pamb

# Sweep Ethanol from 80% down to 30% in steps of 10%
for eth_pct in range(80, 29, -10):
    pg_pct = 100 - eth_pct
    
    fuel_name = f"Blend_{eth_pct}_{pg_pct}"
    
    # Create the card for this specific mixture dynamically
    custom_fuel_card = f"""
    fuel Ethanol         C 2.0 H 6.0 O 1.0  wt%={eth_pct:.1f}  h,cal=-66370.0   t(k)=298.15  rho=0.789
    fuel PropGlycol      C 3.0 H 8.0 O 2.0  wt%={pg_pct:.1f}  h,cal=-115153.0  t(k)=298.15  rho=1.036
    """
    
    try:
        add_new_fuel(fuel_name, custom_fuel_card)
    except Exception:
        pass # Suppress duplicate registrations if run multiple times
        
    C = CEA_Obj( oxName='GOX', fuelName=fuel_name, 
                 pressure_units='bar', 
                 cstar_units='m/s', 
                 temperature_units='K', 
                 isp_units='sec',
                 density_units='kg/m^3',
                 specific_heat_units='J/kg-K')
                 
    best_MR_vac = 0
    best_IspVac = 0
    
    # Sweep O/F Mixture ratios from 1.0 to 3.5 in increments of 0.5
    for mr_int in range(10, 36, 5):
        mr = mr_int / 10.0
        
        try:
            eps = C.get_eps_at_PcOvPe(Pc=Pc, MR=mr, PcOvPe=Pc_over_Pe)
        except Exception:
            continue
            
        if eps is None or eps <= 1.0:
            continue
            
        IspAmb, mode = C.estimate_Ambient_Isp(Pc=Pc, MR=mr, eps=eps, Pamb=Pamb)
        IspVac, Cstar, Tc, mw, gam = C.get_IvacCstrTc_ChmMwGam(Pc=Pc, MR=mr, eps=eps)
        
        mdot = thrust_target / (IspAmb * g0)
        Pc_Pa = Pc * 100000.0
        At_m2 = (Cstar * mdot) / Pc_Pa
        At_cm2 = At_m2 * 10000.0
        Ae_cm2 = At_cm2 * eps

        print(f"{eth_pct}/{pg_pct:<12} {mr:<8.1f} {IspAmb:<12.2f} {IspVac:<12.2f} {gam:<10.4f} {Tc:<8.1f} {eps:<8.3f} {mdot:<12.4f} {At_cm2:<10.3f} {Ae_cm2:<10.3f}")

    print("-" * 115)
