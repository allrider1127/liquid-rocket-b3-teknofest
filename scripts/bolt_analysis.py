# scripts/tie_rod_analysis.py
import math

def analyze_tie_rods():
    print(f"{'--- KOR B3 TIE-ROD STRUCTURAL ANALYSIS ---':^45}")
    
    # Inputs
    Pc_pa = 10.0 * 100000.0   # 10 bar chamber pressure
    D_seal_m = 0.050          # 50mm seal diameter (based on your mechanical seal)
    num_rods = 4              # Your 4 steel shafts
    rod_dia_mm = 8            # Assume 8mm steel rods (M8 threaded rods)
    steel_yield_mpa = 250.0   # Yield strength for standard A307/Mild Steel
    
    # 1. Calculate the force trying to push the engine apart
    area_seal = math.pi * (D_seal_m / 2)**2
    f_blow_off = Pc_pa * area_seal
    
    # 2. Calculate the capacity of your 4 steel shafts
    rod_area = math.pi * ((rod_dia_mm / 1000) / 2)**2
    total_steel_area = rod_area * num_rods
    total_capacity_n = steel_yield_mpa * 1e6 * total_steel_area
    
    # 3. Safety Factor
    sf = total_capacity_n / f_blow_off
    
    print(f"Internal Pressure Area (50mm): {area_seal*1e6:.2f} mm^2")
    print(f"Total Separation Force:        {f_blow_off:.2f} N")
    print(f"Total Tie-Rod Capacity:        {total_capacity_n:.2f} N")
    print(f"Structural Safety Factor (SF): {sf:.2f}")
    print("-" * 45)
    
    if sf > 3.0:
        print("STATUS: Design is highly secure for 10 bar operation.")
    else:
        print("STATUS: Increase rod diameter or use higher grade steel.")

if __name__ == "__main__":
    analyze_tie_rods()
