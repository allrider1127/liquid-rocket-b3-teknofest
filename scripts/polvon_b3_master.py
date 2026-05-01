import numpy as np

from run_gox_isopar_h import (
    Pc, best_Tc, best_Cstar, mdot_f, mdot_ox, best_IspAmb, best_At_cm2, best_Ae_cm2
)
from injector_priming import tau_f, tau_ox

def generate_report_table():
    print(f"\n{'='*68}")
    print(f"{'KOR B3 PROJECT - FINAL PERFORMANCE SUMMARY TABLE':^68}")
    print(f"{'='*68}")

    header = ['Parameter Description', 'Symbol', 'Value', 'Unit']
    data = [
        ['Target Thrust (Ambient)', 'F_amb', '100.0', 'N'],
        ['Chamber Pressure', 'Pc', f"{Pc:.1f}", 'bar'],
        ['Combustion Temperature', 'Tc', f"{best_Tc:.1f}", 'K'],
        ['Characteristic Velocity', 'C*', f"{best_Cstar:.1f}", 'm/s'],
        ['Specific Impulse (Aksaray)', 'Isp', f"{best_IspAmb:.1f}", 's'],
        ['Throat Area', 'At', f"{best_At_cm2:.4f}", 'cm^2'],
        ['Exit Area', 'Ae', f"{best_Ae_cm2:.4f}", 'cm^2'],
        ['Fuel Mass Flow (Isopar-H)', 'mdot_f', f"{mdot_f:.5f}", 'kg/s'],
        ['Oxidizer Mass Flow (GOX)', 'mdot_ox', f"{mdot_ox:.5f}", 'kg/s'],
        ['---', '---', '---', '---'],
        ['Fuel Priming Delay', 'tau_f', f"{tau_f:.2f}", 'ms'],
        ['Oxidizer Priming Delay', 'tau_ox', f"{tau_ox:.2f}", 'ms'],
        ['Ignition Sequence Lead', 'Lead', f"{tau_f - tau_ox:.2f}", 'ms (Ox-Lead)']
    ]

    w = [32, 10, 12, 12]
    head_str = f"{header[0]:<{w[0]}} | {header[1]:<{w[1]}} | {header[2]:<{w[2]}} | {header[3]:<{w[3]}}"
    print(head_str)
    print("-" * 68)

    for row in data:
        if row[0] == '---':
            print("-" * 68)
            continue
        row_str = f"{row[0]:<{w[0]}} | {row[1]:<{w[1]}} | {row[2]:<{w[2]}} | {row[3]:<{w[3]}}"
        print(row_str)

    print(f"{'='*68}\n")

if __name__ == "__main__":
    generate_report_table()
