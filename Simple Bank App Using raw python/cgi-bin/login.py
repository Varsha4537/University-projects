#!/usr/bin/env python3
import os, sys, json, uuid
from urllib.parse import parse_qs, unquote

print("Content-Type: text/html\n")

USERS_FILE = "cgi-bin/users.json"
SESSION_FILE = "cgi-bin/sessions.json"

# Load users
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {}

# Read POST data
length = int(os.environ.get("CONTENT_LENGTH", 0))
post_data = sys.stdin.read(length)
params = parse_qs(post_data)

username = params.get("username", [""])[0]
password = params.get("password", [""])[0]

# Handle return URL
query = os.environ.get("QUERY_STRING", "")
return_to = "http://localhost:8080/index"
if query.startswith("return_to="):
    return_to = unquote(query.split("=", 1)[1]).rstrip('/').removesuffix('.py')
    if return_to.endswith('.py'):
        return_to = return_to[:-3]

# Validate user
if username in users and users[username] == password:
    token = str(uuid.uuid4())
    with open(SESSION_FILE, "r") as f:
        sessions = json.load(f)
    sessions[token] = username
    with open(SESSION_FILE, "w") as f:
        json.dump(sessions, f)

    # ✅ Print username in header so login_server.py can extract it
    print(f"X-Username: {username}")
    print("Status: 302 Found")
    print(f"Location: {return_to}")
    print(f"Set-Cookie: session={token}; Path=/")
    print("Content-Type: text/html\n")
    print("<html><body>Redirecting...</body></html>")
else:
    print("<h1>Login failed. Invalid username or password.</h1>")
    print("DEBUG:", username, password, users.get(username), file=sys.stderr)







