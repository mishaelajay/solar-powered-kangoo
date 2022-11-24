import paho.mqtt.client as mqtt  # import the client1
import time
import sqlite3

target_topic = 'solpiplog/pylon/pack1/soc'


def on_log(client, userdata, level, buf):
    k = 0


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected ok")
    else:
        print("not connected", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print("disconnect result code " + str(rc))


def on_message(client, userdata, msg):
    global m_decode
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    time.sleep(1)

    msg_value = str(m_decode)

    if msg.topic == target_topic:
        insert_into_db(msg_value)

    key_value_row = '{dyn_key}:{dyn_value}'.format(dyn_key=msg.topic, dyn_value=msg_value)

    print("Battery Values-------------->", key_value_row)
    # Store these values to db
    mqtt_test_file = open("battery_values.txt", "a")
    mqtt_test_file.write(key_value_row + "\n")
    mqtt_test_file.close()


def insert_into_db(msg_value):
    with sqlite3.connect("solar_powered_kangoo.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO battery_values(soc) VALUES(?)", msg_value)
        con.commit()
        msg = "Record successfully added"


broker_address = "127.0.0.1:1883"
client = mqtt.Client("paca")  # create new instance
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_log = on_log
client.on_message = on_message

print("cnct to broker", broker_address)
client.connect("127.0.0.1", 1883, 60)
client.subscribe([("solpiplog/pylon/#", 2)])

client.loop_forever()
