import numpy as np
from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_fuel

# -------------------------------
# 1. DEFINE FUEL
# -------------------------------
custom_fuel_card = """
fuel IsoparH  C 12.0 H 26.0  wt%=100.0  h,cal=-65000.0  t(k)=298.15  rho=0.76
"""
add_new_fuel('IsoparH', custom_fuel_card)

C = CEA_Obj(
    oxName='GOX',
    fuelName='IsoparH',
    pressure_units='bar',
    cstar_units='m/s',
    temperature_units='K',
    isp_units='sec'
)

# -------------------------------
# 2. IMPORT PINTLE DATA
# -------------------------------
from pintle_dimension import (
    A_inj_f,
    A_inj_ox,
    Cd_f,
    Cd_ox,
    rho_f,
    rho_ox,
    MR_design
)

# -------------------------------
# 3. ENGINE CONSTANTS
# -------------------------------
g0 = 9.80665

At_cm2 = 0.50  # replace with your real value if needed
At = At_cm2 / 10000.0

eps = 2.5
P_tank = 20.0  # bar


# -------------------------------
# 4. SOLVER
# -------------------------------
def solve_engine():

    Pc = 10.0  # initial guess

    print("\nITERATION START")
    print("-" * 60)

    for i in range(30):

        dP = (P_tank - Pc) * 1e5
        if dP <= 0:
            print("Flow stopped: tank pressure <= chamber pressure")
            break

        mdot_f = Cd_f * A_inj_f * np.sqrt(2 * rho_f * dP)
        mdot_ox = Cd_ox * A_inj_ox * np.sqrt(2 * rho_ox * dP)

        mdot_total = mdot_f + mdot_ox
        MR_real = mdot_ox / mdot_f

        IspVac, Cstar, Tc, mw, gam = C.get_IvacCstrTc_ChmMwGam(
            Pc=Pc,
            MR=MR_real,
            eps=eps
        )

        Pc_new = (mdot_total * Cstar) / At / 1e5

        thrust = mdot_total * IspVac * g0 * 0.9

        print(f"Iter {i:02d} | Pc: {Pc_new:6.2f} bar | Thrust: {thrust:7.2f} N | MR: {MR_real:.2f}")

        if abs(Pc_new - Pc) < 0.01:
            print("\nCONVERGED")
            print(f"Final Pc      : {Pc_new:.2f} bar")
            print(f"Final Thrust  : {thrust:.2f} N")
            print(f"Final MR      : {MR_real:.2f}")
            print(f"C*            : {Cstar:.2f} m/s")
            print(f"Isp (vac)     : {IspVac:.2f} s")
            return

        Pc = Pc_new

    print("\nDid not converge")


# -------------------------------
# 5. RUN
# -------------------------------
if __name__ == "__main__":
    solve_engine()
