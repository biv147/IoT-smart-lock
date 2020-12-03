import paho.mqtt.client as mqtt
from flask import Flask, request, render_template, redirect
import time
import pyrebase



firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# flask name
app = Flask(__name__)

email = ""
password = ""

status = ""


# callback function to retrieve message
def on_message(client, userdata, message):
    print("Data recieved: " + str(message.payload.decode("utf-8")))
    print("Topic=", message.topic)
    store_state(str(message.payload.decode("utf-8")))


# callback function to connect to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected!\n")
    else:
        print("Unable to connect!\n")
    client.subscribe("LockState")
    return client


def store_state(state):
    global status
    status = state


def return_state():
    return status



# creating the client and connecting it
client = mqtt.Client()
print("Connecting to broker...")
time.sleep(1)

# subscribing and getting the messages
client.on_connect = on_connect
client.on_message = on_message

# connect to broker
client.connect("localhost", 1833, 60)


# starting the loop
client.loop_start()


# endpoints
@app.route("/sign_up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        req = request.form

        email = req.get("user")
        password = req.get("pass")
        confirmpassword = req.get("confirmpass")

        print("Email: "+email)
        print("Password: "+password)

        if (len(password) >= 6):
            if (password == confirmpassword):
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    print("User has been added")
                    return redirect('http://127.0.0.1:5000/')
                except:
                    print("unable to add user")
            else:
                print("Passwords do not match")
                #return redirect('http://127.0.0.1:5000/sign_up')
        else:
            print("Password must be 6 characters long minimum")

    return render_template('sign_up.html')


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        req = request.form

        email = req.get("user")
        password = req.get("pass")

        print("email: " + email)
        print("Password: " + password)

        try:
            login = auth.sign_in_with_email_and_password(email, password)
            print("logged in")
            return redirect("http://127.0.0.1:5000/lock_status")
        except:
            print("invalid user")

    return render_template('home.html')


@app.route("/lock_status", methods=["POST", "GET"])
def lock():
    if request.method == "POST":
        if request.form['state'] == 'lock':
            print("locked")
            client.publish("Data", "locked")

            return redirect("http://127.0.0.1:5000/lock_status")

        elif request.form['state'] == 'unlock':
            print("unlocked")
            client.publish("Data", "unlocked")

            return redirect("http://127.0.0.1:5000/lock_status")

    return render_template('lock_status.html', data=return_state())


# running flask
if __name__ == '__main__':
    app.run()
