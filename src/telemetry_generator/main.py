import time
import Position
import ss_telem
import mqtt_publisher

def main():

    mqtt_publisher.publish_telemetry()
     
if __name__ == "__main__":
    main()
