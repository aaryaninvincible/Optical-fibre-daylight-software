"""
HardwareSerialBridge - Microcontroller & IoT Sensor Integration Layer
Interfaces with physical microcontrollers (ESP32, Arduino, Raspberry Pi, STM32)
via UART Serial or JSON WebSocket telemetry to bridge real hardware into the Digital Twin.
"""

import json
import time
import sys

class HardwareSerialBridge:
    def __init__(self, port: str = "COM3", baudrate: int = 115200, mock_mode: bool = True):
        self.port = port
        self.baudrate = baudrate
        self.mock_mode = mock_mode
        self.serial_conn = None

    def connect(self):
        if self.mock_mode:
            print(f"[BRIDGE] Initialized Mock Hardware Bridge on {self.port} (Simulated ESP32 Firmware v1.4)")
            return True
        try:
            import serial
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1.0)
            print(f"[BRIDGE] Connected to physical hardware on {self.port} at {self.baudrate} baud.")
            return True
        except Exception as e:
            print(f"[BRIDGE ERROR] Failed to connect to serial port {self.port}: {e}")
            return False

    def read_sensor_packet(self):
        """
        Reads standardized JSON sensor packet:
        {
            "device_id": "SOLARFIBER_NODE_01",
            "ambient_temp_C": 29.4,
            "focal_temp_C": 52.1,
            "outdoor_lux": 68400,
            "pyranometer_GHI": 845.2,
            "fiber_opt_power_W": 16.4,
            "indoor_lux": 490,
            "pir_occupancy": 1,
            "tracker_azimuth_deg": 182.4,
            "tracker_altitude_deg": 68.2
        }
        """
        if self.mock_mode:
            # Mock telemetry packet
            return {
                "device_id": "SOLARFIBER_NODE_01",
                "ambient_temp_C": 29.4,
                "focal_temp_C": 52.1,
                "outdoor_lux": 68400,
                "pyranometer_GHI": 845.2,
                "fiber_opt_power_W": 16.4,
                "indoor_lux": 490,
                "pir_occupancy": 1,
                "tracker_azimuth_deg": 182.4,
                "tracker_altitude_deg": 68.2,
                "status": "NOMINAL"
            }
        
        if self.serial_conn and self.serial_conn.is_open:
            line = self.serial_conn.readline().decode('utf-8').strip()
            if line:
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    return None
        return None

    def send_actuator_commands(self, target_alt_deg: float, target_az_deg: float, led_pwm_dim: float, shutter_open: bool):
        """
        Transmits control commands to dual-axis stepper motor drivers and LED constant-current PWM buck driver.
        """
        payload = {
            "cmd": "ACTUATE",
            "target_alt": round(target_alt_deg, 2),
            "target_az": round(target_az_deg, 2),
            "led_pwm": round(led_pwm_dim, 3), # 0.0 to 1.0
            "thermal_shutter": 1 if shutter_open else 0
        }
        json_str = json.dumps(payload)
        
        if self.mock_mode:
            print(f"[TX COMMAND] -> {json_str}")
        elif self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.write((json_str + "\n").encode('utf-8'))

if __name__ == "__main__":
    bridge = HardwareSerialBridge(mock_mode=True)
    bridge.connect()
    print("\nReading incoming sensor packet:")
    pkt = bridge.read_sensor_packet()
    print(json.dumps(pkt, indent=2))
    print("\nSending AI controller actuation command:")
    bridge.send_actuator_commands(target_alt_deg=45.2, target_az_deg=180.0, led_pwm_dim=0.15, shutter_open=True)
