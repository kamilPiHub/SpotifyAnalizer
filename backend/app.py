from dotenv import load_dotenv # type: ignore
load_dotenv()

import os
import requests
from flask import Flask, request, redirect, session, jsonify, url_for
from flask_cors import CORS # type: ignore
from datetime import datetime
from requests_oauthlib import OAuth2Session # type: ignore
from oauthlib.oauth2.rfc6749.errors import OAuth2Error # type: ignore

# --- Konfiguracja ---
app = Flask(__name__)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # zmiana z 'None' na 'Lax' dla localhost
app.config['SESSION_COOKIE_SECURE'] = False    # zmiana na False dla localhost
app.config['SESSION_COOKIE_DOMAIN'] = None     # None = domyślnie bieżąca domena
app.config['SECRET_KEY'] = 'taconafide'

CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8081/callback"
FRONTEND_URL = "http://localhost:3000"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"
SCOPE = "user-read-private user-read-email user-top-read user-read-recently-played"

def make_oauth_session(token=None, state=None):
    return OAuth2Session(
        CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE.split(),
        token=token,
        state=state,
        auto_refresh_url=TOKEN_URL,
        auto_refresh_kwargs={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
        token_updater=token_updater
    )

def token_updater(token):
    session['oauth_token'] = token

# --- Trasy Autoryzacji ---

@app.route("/login")
def login():
    oauth = make_oauth_session()
    authorization_url, state = oauth.authorization_url(AUTH_URL, show_dialog=True)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    if 'error' in request.args:
        return redirect(f"{FRONTEND_URL}/?error={request.args['error']}")

    oauth = make_oauth_session(state=session.get('oauth_state'))
    try:
        token = oauth.fetch_token(
            TOKEN_URL,
            client_secret=CLIENT_SECRET,
            authorization_response=request.url
        )
    except OAuth2Error as e:
        print("OAuth2Error:", str(e))
        print("Request args:", dict(request.args))
        print("Session state:", session.get('oauth_state'))
        return redirect(f"{FRONTEND_URL}/?error=token_fetch_failed")
    except Exception as e:
        print("Exception:", str(e))
        print("Request args:", dict(request.args))
        print("Session state:", session.get('oauth_state'))
        return redirect(f"{FRONTEND_URL}/?error=token_fetch_failed")

    session['oauth_token'] = token
    session['expires_at'] = token.get('expires_at', datetime.now().timestamp() + token.get('expires_in', 0))
    return redirect(f"{FRONTEND_URL}/dashboard")

@app.route("/api/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})

@app.route("/api/check-auth", methods=["GET"])
def check_auth():
    if not get_spotify_headers():
        return jsonify({"error": "Not authenticated"}), 401
    return jsonify({"message": "User is authenticated"}), 200

# --- API Endpoints dla Frontendu ---

def get_spotify_headers():
    token = session.get('oauth_token')
    if not token or token.get('expires_at', 0) < datetime.now().timestamp():
        return None
    return {"Authorization": f"Bearer {token['access_token']}"}

@app.route("/api/profile")
def get_profile():
    headers = get_spotify_headers()
    if not headers:
        return jsonify({"error": "Not authenticated"}), 401
    response = requests.get(API_BASE_URL + "me", headers=headers)
    return jsonify(response.json())

@app.route("/api/top-tracks")
def get_top_tracks():
    headers = get_spotify_headers()
    if not headers:
        return jsonify({"error": "Not authenticated"}), 401
    params = {
        "time_range": request.args.get("time_range", "medium_term"),
        "limit": request.args.get("limit", 20)
    }
    response = requests.get(API_BASE_URL + "me/top/tracks", headers=headers, params=params)
    return jsonify(response.json())

@app.route("/api/top-artists")
def get_top_artists():
    headers = get_spotify_headers()
    if not headers:
        return jsonify({"error": "Not authenticated"}), 401
    params = {
        "time_range": request.args.get("time_range", "medium_term"),
        "limit": request.args.get("limit", 20)
    }
    response = requests.get(API_BASE_URL + "me/top/artists", headers=headers, params=params)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(port=8081, debug=True)