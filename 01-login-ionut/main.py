"""Python Flask WebApp Auth0 integration example
"""
import subprocess
import os
import base64
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

# sunt elemente in connection daca sunt libere
# la inceput sunt toate conexiunile
connections = []

def allocate_and_get_connection():

    if "connection" not in session or session["connection"] is None:
        if len(connections) == 0:
            return None
        connection = connections.pop()
        print("Retrieved connection")
        session["connection"] = connection
        return connection
    else:
        return session["connection"]


def release_connection(connection):
    connections.append(connection)
    session["connection"] = None
    return True

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")


oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


# Controllers API
@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("dashboard", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/connect", methods=["GET", "POST"])
def connect_user():
    # Retrieve connection details from WireGuard
    connection = allocate_and_get_connection()
    
    if connection is None:
        return "No connections available, please try again later"
    session["connection"] = connection
    print("User connected to WireGuard via connection: " + connection)
    return "User connected to WireGuard via connection: " + connection
    


@app.route("/disconnect", methods=["GET", "POST"])
def disconnect_user():
    #retrieve connection details from local storage
    connection = session["connection"]
    #release the connection
    release_connection(connection)
    #remove the connection from local storage
    session["connection"] = None
    print("User disconnected from WireGuard, dropping connection " + connection)
    return"User disconnected from WireGuard, dropping connection " + connection




connections.append("<br>[Interface]<br>\
PrivateKey = S72aqA3SUpxEqZUM4OMw9g3cOXxRM7WQtz9UQVXd4CM=<br>\
Address = 192.168.100.2/24<br>\
[Peer]<br>\
PublicKey = dvuW9BsRWOr7rzpq1HSnur1MQEaIWfPo9iHSO4faW0I==<br>\
AllowedIPs = 0.0.0.0/0<br>\
Endpoint = 34.163.137.25:51820<br>")

connections.append("<br>[Interface]<br>\
PrivateKey = IVs8itFO4NXBEpGWns4u8peoL8Wpr91eCPo3oSyp+HU=<br>\
Address = 192.168.101.2/24<br>\
[Peer]<br>\
PublicKey = dvuW9BsRWOr7rzpq1HSnur1MQEaIWfPo9iHSO4faW0I=<br>\
AllowedIPs = 0.0.0.0/0<br>\
Endpoint = 34.163.137.25:51820<br>")

connections.append("<br>[Interface]<br>\
PrivateKey = B9apoNGZm4ev3R994fXmu2yd+qGOv7B1CoUrVFWKRVI=<br>\
Address = 192.168.102.2/24<br>\
[Peer]<br>\
PublicKey = dvuW9BsRWOr7rzpq1HSnur1MQEaIWfPo9iHSO4faW0I=<br>\
AllowedIPs = 0.0.0.0/0<br>\
Endpoint = 34.163.137.25:51820<br>")

connections.append("<br>[Interface]<br>\
PrivateKey = xGfWpT2Fk5r7HZL8ucximmGzclW4ke2Xu9B3qxM9On8=<br>\
Address = 192.168.103.2/24<br>\
[Peer]<br>\
PublicKey = dvuW9BsRWOr7rzpq1HSnur1MQEaIWfPo9iHSO4faW0I=<br>\
AllowedIPs = 0.0.0.0/0<br>\
Endpoint = 34.163.137.25:51820<br>")

connections.append("<br>[Interface]<br>\
PrivateKey = HaLNA/JdavSbVhoCaJ99cl99yb662AZ/f1k4vn8twSE=<br>\
Address = 192.168.104.2/24<br>\
[Peer]<br>\
PublicKey = dvuW9BsRWOr7rzpq1HSnur1MQEaIWfPo9iHSO4faW0I=<br>\
AllowedIPs = 0.0.0.0/0<br>\
Endpoint = 34.163.137.25:51820<br>")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))




