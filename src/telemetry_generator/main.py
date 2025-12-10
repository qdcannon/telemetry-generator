import time
import Position
import ss_telem

def main():

    #initial tvalues
    current_position = Position.get_initial_position()
    current_velocity = Position.get_initial_velocity()

    while True:
        # Compute acceleration

        current_position, current_velocity = Position.update_position(current_position,current_velocity)
        current_voltage, current_temperature_c = ss_telem.update_ss_telem()
        ss_telem.packetize_telemetry(current_position, current_velocity,current_voltage, current_temperature_c)

        time.sleep(1)

if __name__ == "__main__":
    main()
