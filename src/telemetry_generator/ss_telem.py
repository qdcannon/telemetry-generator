import random
import json
import time
from vector_class import Vector


def update_ss_telem(): 
# Simulated subsystem telemetry
    battery_power = 28.0 - 0.001 * random.random()
    temperature_c = 60.0 + random.uniform(-1.0, 2.0)

    return battery_power, temperature_c

def packetize_telemetry(position: Vector, velocity: Vector, voltage: float, temp_c: float):
    telemetry_packet = {
        "timestamp": int(time.time()),
        "position_km": position.to_list(),
        "velocity_km_s": velocity.to_list(),
        "battery_voltage": round(voltage, 3),
        "temperature_c": round(temp_c, 2),
        "attitude_deg": [
            round(random.uniform(-2.0, 2.0), 2),
            round(random.uniform(-2.0, 2.0), 2),
            round(random.uniform(-2.0, 2.0), 2),
        ]
    }

    # Emit telemetry as JSON (stdout)
    print(json.dumps(telemetry_packet))