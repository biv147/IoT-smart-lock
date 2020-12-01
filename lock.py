import paho.mqtt.client as mqtt
import time

lock_status = "nothing"

#callback function to retrieve message
def on_message(client, userdata, message):
    print("Data recieved: "+ str(message.payload.decode("utf-8")))
    #print("message topic=", message.topic)
    chageStatus(client, str(message.payload.decode("utf-8")))

#callback function to connect to the broker
def on_connect(client, userdata, flags, rc):
    print("connected ok!")
    client.subscribe("Data")


def chageStatus(client, status):
    lock_status = status
    print(lock_status)
    client.publish("LockState", lock_status)


def main():
    # creating the client and connecting the client
    client = mqtt.Client()
    client.connect("localhost", 1833, 60)
    print("lock connected to broker")

    client.on_connect = on_connect
    client.on_message = on_message

    # val = input("Enter what you want to send: ")
    # val = "hello"

    print(lock_status)
    client.publish("LockState", lock_status)

    time.sleep(5)

    client.loop_forever()

if __name__ == '__main__':
    main()