import os
import requests
import urllib.parse
from dotenv import load_dotenv # type: ignore
from flask import Flask, request, redirect, jsonify
from flask_cors import CORS # type: ignore

load_dotenv()

app = Flask(__name__)
# W tym modelu nie potrzebujemy już SECRET_KEY, bo nie używamy sesji Flask
CORS(app, origins=["http://localhost:3000"])

# --- Stałe Spotify ---
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"
FRONTEND_URL = "http://localhost:3000"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"
SCOPE = "user-read-private user-read-email user-top-read user-read-recently-played"

# --- Logika Autoryzacji ---

@app.route("/login")
def login():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "show_dialog": True
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    if 'error' in request.args:
        return redirect(f"{FRONTEND_URL}/?error={request.args['error']}")
    
    if 'code' in request.args:
        req_body = {
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        # KLUCZOWA ZMIANA: Przekazujemy tokeny do frontendu jako parametry URL
        access_token = token_info["access_token"]
        refresh_token = token_info["refresh_token"]
        expires_in = token_info["expires_in"]
        
        # Przekieruj do specjalnej ścieżki na frontendzie, która przechwyci tokeny
        return redirect(f"{FRONTEND_URL}/auth/callback?access_token={access_token}&refresh_token={refresh_token}&expires_in={expires_in}")

# --- API Endpoints ---
# Zwróć uwagę, że nie ma tu już logiki sesji!

@app.route("/api/profile")
def get_profile():
    # Oczekujemy nagłówka: Authorization: Bearer <access_token>
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Authorization header required"}), 401
    
    try:
        access_token = auth_header.split(" ")[1]
    except IndexError:
        return jsonify({"error": "Invalid Authorization header format"}), 401

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(API_BASE_URL + "me", headers=headers)
    return jsonify(response.json()), response.status_code

@app.route("/api/top-tracks")
def get_top_tracks():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Authorization header required"}), 401
    access_token = auth_header.split(" ")[1]
    
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"time_range": request.args.get("time_range", "medium_term"), "limit": 50}
    response = requests.get(API_BASE_URL + "me/top/tracks", headers=headers, params=params)
    return jsonify(response.json()), response.status_code

# Endpoint do odświeżania tokenu - teraz jest to konieczne!
@app.route('/api/refresh-token')
def refresh_token():
    refresh_token = request.args.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'Refresh token is required'}), 400

    req_body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=req_body)
    return jsonify(response.json()), response.status_code


if __name__ == "__main__":
    app.run(port=5000)