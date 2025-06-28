#!/usr/bin/env python3
import os
import json
import inspect

SESSIONS_FILE = "cgi-bin/sessions.json"

def load_sessions():
    if not os.path.exists(SESSIONS_FILE):
        return {}
    with open(SESSIONS_FILE, 'r') as f:
        return json.load(f)

# Extract session ID from cookie
cookie = os.environ.get("HTTP_COOKIE", "")
session_id = ""
for part in cookie.split(";"):
    if "session=" in part:
        session_id = part.strip().split("=")[1]

#Validate session
sessions = load_sessions()
username = sessions.get(session_id)

if not username:
    print("Content-Type: text/html\n")
    print("<h1>Unauthorized. <a href='http://localhost:8081/login'>Login</a></h1>")
    exit()

#Load user-specific balance
balance_file = f"balance_{username}.txt"
try:
    with open(balance_file, "r") as f:
        balance = int(f.read().strip())
except:
    balance = 0

#Print HTML
#print("Content-Type: text/html\n")
print(f"<h1>Bank Dashboard for {username}</h1>")
print(f"<p>Balance: {balance}</p>")

print(f"""
<form action="add" method="POST">
  <input type="hidden" name="user" value="{username}">
  <input type="number" name="amount" value="100">
  <input type="submit" value="Add Money">
</form>
<form action="remove" method="POST">
  <input type="hidden" name="user" value="{username}">
  <input type="number" name="amount" value="50">
  <input type="submit" value="Remove Money">
</form>
""")

print("<a href='http://localhost:8081/logout?return_to=http://localhost:8080/index'>Logout</a>")


