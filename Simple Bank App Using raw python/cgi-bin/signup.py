#!/usr/bin/env python3
import os, sys, json, uuid
from urllib.parse import parse_qs, unquote

USERS_FILE = "cgi-bin/users.json"
SESSIONS_FILE = "cgi-bin/sessions.json"

# Read users
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

# Get return_to URL
query = os.environ.get("QUERY_STRING", "")
return_to = "http://localhost:8080/index"
if query.startswith("return_to="):
    return_to = unquote(query.split("=", 1)[1]).rstrip('/').removesuffix('.py')
    if return_to.endswith('.py'):
        return_to = return_to[:-3]

# Validate input
if not username or not password:
    print("\n<h1>Signup failed. Missing username or password.</h1>")
    exit()

# Save user
users[username] = password
with open(USERS_FILE, 'w') as f:
    json.dump(users, f)

# Create session
session_id = str(uuid.uuid4())

# Load existing sessions
if os.path.exists(SESSIONS_FILE):
    with open(SESSIONS_FILE, 'r') as f:
        sessions = json.load(f)
else:
    sessions = {}

sessions[session_id] = username

# Save updated sessions
with open(SESSIONS_FILE, 'w') as f:
    json.dump(sessions, f)

# Proper HTTP response with headers
print(f"X-Username: {username}")
print("Status: 302 Found")
print(f"Location: {return_to}")
print(f"Set-Cookie: session={session_id}; Path=/")
print("Content-Type: text/html")
print("<html><body>Redirecting" \
"...</body></html>")

