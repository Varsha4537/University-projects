#!/usr/bin/env python3
import os, sys, json
import urllib.parse

SESSIONS_FILE = "cgi-bin/sessions.json"

def load_sessions():
    if not os.path.exists(SESSIONS_FILE):
        return {}
    with open(SESSIONS_FILE, "r") as f:
        return json.load(f)

#Get session ID from cookie
cookie = os.environ.get("HTTP_COOKIE", "")
session_id = ""
for part in cookie.split(";"):
    if "session=" in part:
        session_id = part.strip().split("=")[1]

#Validate session and get username
sessions = load_sessions()
username = sessions.get(session_id)

if not username:
    print("Content-Type: text/html\n")
    print("<h1>Unauthorized</h1>")
    exit()

# Get posted amount
length = int(os.environ.get("CONTENT_LENGTH", 0))
post_data = sys.stdin.read(length)
# Parse the form data safely
parsed_data = urllib.parse.parse_qs(post_data)
amount_str = parsed_data.get('amount', ['0'])[0]
try:
    amount = int(amount_str)
except ValueError:
    amount = 0

#Load and update user balance
BALANCE_DIR = os.path.dirname('cgi-bin/balances/')
balance_file = os.path.join(BALANCE_DIR, f"balance_{username}.txt")
try:
    with open(balance_file, "r") as f:
        balance = int(f.read().strip())
except:
    balance = 0

balance += amount

with open(balance_file, "w") as f:
    f.write(str(balance))


print("Content-Type: text/html\n")
print(f"<p>Added {amount} to {username}'s account.</p>")
print("<a href='dashboard'>Back</a>")

