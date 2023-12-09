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



@app.route("/connect", methods=["POST"])
def connect_user(username):
    # Replace this with the actual path to your WireGuard configuration directory
    config_dir = "/path/to/wireguard/configs"

    # Generate a new WireGuard private key for the user
    private_key = subprocess.check_output(["wg", "genkey"]).decode("utf-8").strip()

    # Derive the public key from the private key
    public_key = subprocess.check_output(["wg", "pubkey"], input=private_key.encode("utf-8")).decode("utf-8").strip()

    # Create a WireGuard configuration file for the user
    config_content = f"""
    [Interface]
    PrivateKey = {private_key}
    Address = 10.0.0.2/32
    DNS = 8.8.8.8

    [Peer]
    PublicKey = {base64.b64encode(public_key.encode('utf-8')).decode('utf-8')}
    AllowedIPs = 0.0.0.0/0
    Endpoint = your_wireguard_server_ip:51820
    """

    user_config_path = os.path.join(config_dir, f"{username}.conf")

    with open(user_config_path, "w") as config_file:
        config_file.write(config_content)

    # Add the user's public key to the WireGuard server configuration (replace with your actual server configuration)
    subprocess.run(["wg", "set", "wg0", "peer", public_key, "allowed-ips", "10.0.0.2/32"])

    return f"User connected to WireGuard. Configuration saved to {user_config_path}"







@app.route("/disconnect", methods=["POST"])
def disconnect_user():
    # Implement logic to disconnect a user in WireGuard
    # You may need to read user information from the session
    # and use it to disassociate the user from the WireGuard configuration
    return "User disconnected from WireGuard"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))
