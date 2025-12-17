import time
import paho.mqtt.client as mqtt
import ss_telem
import Position
import json

def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")

def publish_telemetry():
            #initial tvalues
    current_position = Position.get_initial_position()
    current_velocity = Position.get_initial_velocity()

    unacked_publish = set()
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_publish = on_publish

    mqttc.user_data_set(unacked_publish)
    #mqttc.connect("mqtt.eclipseprojects.io")
    mqttc.connect("10.244.0.84")
    #mqttc.loop_start()



    while True:
        # Compute acceleration

        current_position, current_velocity = Position.update_position(current_position,current_velocity)
        current_voltage, current_temperature_c = ss_telem.update_ss_telem()
        telemetry_packet = ss_telem.packetize_telemetry(current_position, current_velocity,current_voltage, current_temperature_c)

        time.sleep(1)

        # Our application produce some messages
        msg_info = mqttc.publish("vehicle/position", json.dumps(telemetry_packet), qos=1)
        unacked_publish.add(msg_info.mid)

        #msg_info2 = mqttc.publish("paho/test/topic", "my message2", qos=1)
        #unacked_publish.add(msg_info2.mid)

        # Wait for all message to be published
        while len(unacked_publish):
            time.sleep(0.1)

        # Due to race-condition described above, the following way to wait for all publish is safer
        msg_info.wait_for_publish()
        #msg_info2.wait_for_publish()

        mqttc.disconnect()
    
    #mqttc.loop_stop()