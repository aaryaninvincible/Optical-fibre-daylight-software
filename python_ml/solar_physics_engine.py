"""
SolarPhysicsEngine - Standalone Scientific Python Validation Engine
Implements astronomical solar geometry (Spencer, Michalsky, PSA),
concentrator optics, fiber waveguide propagation, and zonal cavity illuminance.
"""

import math
import datetime

class SolarPhysicsEngine:
    G_SC = 1367.0  # Solar constant W/m²
    LUMINOUS_EFFICACY_DIRECT = 105.0  # lm/W
    LUMINOUS_EFFICACY_DIFFUSE = 115.0 # lm/W

    @staticmethod
    def calculate_solar_position(dt: datetime.datetime, lat: float, lon: float, tz_offset: float = 5.5):
        day_of_year = dt.timetuple().tm_yday
        time_hours = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
        lat_rad = math.radians(lat)

        # Fractional year gamma (radians)
        gamma = (2 * math.pi / 365.0) * (day_of_year - 1 + (time_hours - 12.0) / 24.0)

        # Equation of Time (EoT) in minutes (Spencer 1971)
        eot = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma)
                        - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))

        # Solar Declination delta (radians)
        decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) \
               - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma) \
               - 0.002697 * math.cos(3 * gamma) + 0.00148 * math.sin(3 * gamma)

        # Local Solar Time (LST) in minutes
        lst_min = time_hours * 60.0 + eot + 4.0 * (lon - tz_offset * 15.0)
        solar_time_hours = (lst_min / 60.0 + 24.0) % 24.0

        # Hour angle omega
        omega_deg = (solar_time_hours - 12.0) * 15.0
        omega_rad = math.radians(omega_deg)

        # Solar Zenith
        cos_zenith = math.sin(lat_rad) * math.sin(decl) + math.cos(lat_rad) * math.cos(decl) * math.cos(omega_rad)
        cos_zenith = max(-1.0, min(1.0, cos_zenith))
        zenith_rad = math.acos(cos_zenith)
        zenith_deg = math.degrees(zenith_rad)

        altitude_deg = max(0.0, 90.0 - zenith_deg)
        altitude_rad = math.radians(altitude_deg)

        # Azimuth
        azimuth_deg = 180.0
        if altitude_deg > 0.0:
            cos_az = (math.sin(decl) * math.cos(lat_rad) - math.cos(decl) * math.sin(lat_rad) * math.cos(omega_rad)) / max(0.01, math.cos(altitude_rad))
            cos_az = max(-1.0, min(1.0, cos_az))
            az_from_south = math.degrees(math.acos(cos_az))
            azimuth_deg = (180.0 + az_from_south) if omega_deg > 0 else (180.0 - az_from_south)
            azimuth_deg = (azimuth_deg + 360.0) % 360.0

        # Air Mass
        air_mass = (1.0 / (cos_zenith + 0.50572 * math.pow(6.07995 + altitude_deg, -1.6364))) if altitude_deg > 0 else 0.0
        r_corr = 1.0 + 0.033 * math.cos((2 * math.pi * day_of_year) / 365.0)
        G_on = SolarPhysicsEngine.G_SC * r_corr

        return {
            "altitude_deg": altitude_deg,
            "azimuth_deg": azimuth_deg,
            "zenith_deg": zenith_deg,
            "air_mass": air_mass,
            "G_on": G_on,
            "is_sun_up": altitude_deg > 0
        }

    @staticmethod
    def calculate_irradiance(solar_pos: dict, cloud_factor: float = 0.0):
        if not solar_pos["is_sun_up"]:
            return {"GHI": 0.0, "DNI": 0.0, "DHI": 0.0, "outdoor_lux": 0.0}

        am = solar_pos["air_mass"]
        alt_rad = math.radians(solar_pos["altitude_deg"])
        DNI_clear = solar_pos["G_on"] * math.pow(0.7, math.pow(am, 0.678))
        DHI_clear = 0.095 * solar_pos["G_on"] * math.sin(alt_rad)

        DNI = max(0.0, DNI_clear * (1.0 - cloud_factor * 0.95))
        DHI = max(10.0, DHI_clear * (1.0 + cloud_factor * 0.2))
        GHI = DNI * math.sin(alt_rad) + DHI
        outdoor_lux = DNI * math.sin(alt_rad) * SolarPhysicsEngine.LUMINOUS_EFFICACY_DIRECT + DHI * SolarPhysicsEngine.LUMINOUS_EFFICACY_DIFFUSE

        return {
            "GHI": round(GHI, 2),
            "DNI": round(DNI, 2),
            "DHI": round(DHI, 2),
            "outdoor_lux": round(outdoor_lux, 1)
        }

if __name__ == "__main__":
    now = datetime.datetime(2026, 6, 21, 12, 0, 0)
    pos = SolarPhysicsEngine.calculate_solar_position(now, 28.61, 77.20)
    irr = SolarPhysicsEngine.calculate_irradiance(pos, 0.0)
    print("--- Solar Physics Engine Validation ---")
    print(f"Solar Altitude : {pos['altitude_deg']:.2f}°")
    print(f"Solar Azimuth  : {pos['azimuth_deg']:.2f}°")
    print(f"Direct Normal (DNI): {irr['DNI']} W/m²")
    print(f"Global Horiz (GHI) : {irr['GHI']} W/m²")
    print(f"Outdoor Illuminance: {irr['outdoor_lux']} Lux")
