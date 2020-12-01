import json
import paho.mqtt.client as mqtt
from flask import Flask, request, render_template, jsonify, redirect
import sqlite3 as sql



#flask name
app = Flask(__name__)

username = ""
password = ""
status = ""

#callback function to retrieve message
def on_message(client, userdata, message):
    print("Data recieved: "+ str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)


#callback function to connect to the broker
def on_connect(client, userdata, flags, rc):
    print("connected ok!")
    client.publish("Data","This is a test")
    client.subscribe("LockState")
    #client.subscribe("Data")


#creating the client and connecting it
client = mqtt.Client()
client.on_message = on_message
print("connecting to broker")
client.connect("localhost", 1833, 60)  # connect to broker

#subsribing and getting the messages
client.on_connect = on_connect
client.on_message = on_message

#starting the loop
client.loop_start()

#endpoints
@app.route("/", methods=["GET","POST"])
def hello_world():
    if request.method == "POST":
        req = request.form

        username = req.get("user")
        password = req.get("pass")

        print(username)
        print(password)

        client.publish("Data", username)

        return redirect(request.url)

    return render_template('home.html')


#running flask
if __name__ == '__main__':
    app.run()

