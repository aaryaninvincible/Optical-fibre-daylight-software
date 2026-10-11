"""
SyntheticDataGenerator - High-Fidelity Multi-Variable Solar Daylighting Dataset Generator
Generates full annual or multi-day time-series data at 5-minute resolution with realistic
weather transitions, solar geometry, optical attenuation, and photometric metrics.
"""

import math
import datetime
import os
import pandas as pd
import numpy as np
from solar_physics_engine import SolarPhysicsEngine

def generate_annual_dataset(output_path: str = "synthetic_daylight_1year.csv", lat: float = 28.61, lon: float = 77.20):
    start_date = datetime.datetime(2026, 1, 1, 0, 0, 0)
    end_date = datetime.datetime(2026, 12, 31, 23, 55, 0)
    delta = datetime.timedelta(minutes=15) # 15-min intervals for 35,040 points

    records = []
    current = start_date

    np.random.seed(42)
    # Autoregressive cloud process
    cloud_state = 0.1

    print(f"Generating synthetic annual daylighting dataset from {start_date} to {end_date}...")

    while current <= end_date:
        solar_pos = SolarPhysicsEngine.calculate_solar_position(current, lat, lon)
        
        # Cloud cover random walk with diurnal convection
        hour = current.hour + current.minute / 60.0
        convection = 0.2 * math.sin(max(0, (hour - 11.0) / 7.0 * math.pi)) if 11.0 <= hour <= 18.0 else 0.0
        cloud_noise = np.random.normal(0, 0.08)
        cloud_state = max(0.0, min(1.0, 0.92 * cloud_state + 0.08 * (0.2 + convection) + cloud_noise))

        irr = SolarPhysicsEngine.calculate_irradiance(solar_pos, cloud_state)

        # Concentrator & Fiber Simulation
        aperture_area = math.pi * (0.8 / 2.0)**2 # 0.502 m²
        tracking_eff = 0.99 if solar_pos["is_sun_up"] else 0.0
        P_focused = irr["DNI"] * aperture_area * 0.88 * tracking_eff

        # Fiber: Quartz 12m, loss 0.035 dB/m
        coupling_eff = 0.82
        fiber_loss_dB = 0.035 * 12.0 + 0.02
        transmission_eff = 10**(-fiber_loss_dB / 10.0)
        P_fiber_out = (P_focused * 0.48) * coupling_eff * transmission_eff

        # Room Lumen Photometrics
        daylight_lumens = P_fiber_out * 220.0 * 0.89
        floor_area = 30.0 # 6x5m
        CU = 0.72
        LLF = 0.88
        daylight_lux = (daylight_lumens * CU * LLF) / floor_area

        # Hybrid LED
        target_lux = 500.0
        occupancy = 1 if (8 <= hour <= 19 and current.weekday() < 5) else 0
        active_target = target_lux if occupancy == 1 else 50.0

        lux_deficit = max(0.0, active_target - daylight_lux)
        led_dimming = min(1.0, (lux_deficit * floor_area) / (CU * LLF * (60.0 * 110.0)))
        led_power = led_dimming * 60.0
        baseline_power = min(60.0, (active_target * floor_area) / (CU * LLF * 110.0))
        power_saved = max(0.0, baseline_power - led_power)
        saving_pct = (power_saved / baseline_power * 100.0) if baseline_power > 0 else 100.0

        records.append({
            "timestamp": current.isoformat(),
            "solar_altitude_deg": round(solar_pos["altitude_deg"], 2),
            "solar_azimuth_deg": round(solar_pos["azimuth_deg"], 2),
            "GHI_W_m2": irr["GHI"],
            "DNI_W_m2": irr["DNI"],
            "DHI_W_m2": irr["DHI"],
            "outdoor_lux": irr["outdoor_lux"],
            "cloud_factor": round(cloud_state, 3),
            "fiber_output_power_W": round(P_fiber_out, 2),
            "daylight_lux": round(daylight_lux, 1),
            "indoor_total_lux": round(daylight_lux + (led_dimming * 60.0 * 110.0 * CU * LLF) / floor_area, 1),
            "occupancy": occupancy,
            "target_lux": active_target,
            "LED_power_W": round(led_power, 2),
            "baseline_LED_power_W": round(baseline_power, 2),
            "energy_saving_percent": round(saving_pct, 1),
            "data_provenance": "Synthetic Physics-Informed Simulation"
        })

        current += delta

    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {len(df)} records saved to {output_path}!")
    return df

if __name__ == "__main__":
    generate_annual_dataset("synthetic_daylight_1year.csv")
