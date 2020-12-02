import json
import paho.mqtt.client as mqtt
from flask import Flask, request, render_template, jsonify, redirect
import sqlite3 as sql
import time

# flask name
app = Flask(__name__)

username = ""
password = ""
status = ""
database = "userdata.db"

Table = """
DROP TABLE IF EXISTS authentication ;
CREATE TABLE authentication (
  username text,
  password text
);
"""

connection = sql.connect(database, check_same_thread=0)
conn = connection.cursor()
sql.complete_statement(Table)
conn.executescript(Table)


# callback function to retrieve message
def on_message(client, userdata, message):
    print("Data recieved: " + str(message.payload.decode("utf-8")))
    print("Topic=", message.topic)
    # store_data(message.payload.decode("utf-8"), message.payload.decode("utf-8"))


# callback function to connect to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected!\n")
    else:
        print("Unable to connect!\n")
    # client.publish("Data","This is a test")
    client.subscribe("LockState")
    # client.subscribe("Data")
    return client


def store_data(username, password):
    conn = connection.cursor()
    print("Storing to database...")
    conn.execute("INSERT INTO authentication VALUES(?,?)", (username, password))
    connection.commit()


def check_auth(username, password):
    conn = connection.cursor()
    print("Checking the database")
    conn.execute("SELECT * FROM authentication WHERE username='%s' AND password='%s'" % (username, password))
    checkUser = conn.fetchone()

    if (checkUser is not None):

        print("Logged in successful")
    else:
        print("Username does not exist")


# creating the client and connecting it
client = mqtt.Client()
# client.on_message = on_message
print("Connecting to broker...")
time.sleep(1)

# subsribing and getting the messages
client.on_connect = on_connect
client.on_message = on_message

# connect to broker
client.connect("localhost", 1833, 60)
store_data("preet", "1234")

# starting the loop
client.loop_start()


# endpoints
@app.route("/sign_up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        req = request.form

        username = req.get("user")
        password = req.get("pass")

        print(username)
        print(password)

        client.publish("Data", username)
        client.publish("Data", password)
        store_data(username, password)

        return redirect('http://127.0.0.1:5000/')

    return render_template('sign_up.html')


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        req = request.form

        username = req.get("user")
        password = req.get("pass")

        print(username)
        print(password)
        check_auth(username, password)

        client.publish("Data", username)
        client.publish("Data", password)

        return redirect(request.url)

    return render_template('home.html')

@app.route("/lock-status", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        req = request.form

        username = req.get("user")
        password = req.get("pass")

        print(username)
        print(password)
        check_auth(username, password)

        client.publish("Data", username)
        client.publish("Data", password)

        return redirect(request.url)

    return render_template('lockstatus')


# running flask
if __name__ == '__main__':
    app.run()

