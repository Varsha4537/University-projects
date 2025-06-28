#!/usr/bin/env python3
import os
import json
import urllib.parse

SESSIONS_FILE = "cgi-bin/sessions.json"

def load_sessions():
    if os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_sessions(sessions):
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f)

# Get session ID from cookie
cookie = os.environ.get("HTTP_COOKIE", "")
session_id = ""
for part in cookie.split(";"):
    if "session=" in part:
        session_id = part.strip().split("=")[1]

# Remove session ID from sessions.json
sessions = load_sessions()
if session_id in sessions:
    del sessions[session_id]
    save_sessions(sessions)

# Redirect to homepage (or return_to if specified)
query = os.environ.get("QUERY_STRING", "")
params = urllib.parse.parse_qs(query)
return_to = params.get("return_to", ["http://localhost:8080/index"])[0]

# Ensure return_to is a valid URL
print("Status: 302 Found")
print(f"Location: {return_to}")
print("Set-Cookie: session=; Path=/; Max-Age=0")
print("Content-Type: text/html")
print() 
print("<html><body>Redirecting...</body></html>")
