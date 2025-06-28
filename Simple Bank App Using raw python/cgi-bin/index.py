#!/usr/bin/env python3
import os
import json

print("Content-Type: text/html\n")

# Get the session cookie
cookie = os.environ.get("HTTP_COOKIE", "")
session = ""
if "session=" in cookie:
    session = cookie.split("session=")[-1].split(";")[0]

# Validate session using sessions.json
username = None
try:
    with open("sessions.json", "r") as f:
        sessions = json.load(f)
    username = sessions.get(session)
except Exception:
    pass

# Render HTML
print("<!DOCTYPE html>")
print("<html>")
print("<head>")
print("<title>Simple Bank</title>")
print("</head>")
print("<body>")

if username:
    print(f"<h1>Welcome back, {username}!</h1>")
    print("<a href='/dashboard'>Go to Dashboard</a><br>")
    print("<a href='http://localhost:8081/logout?return_to=http://localhost:8080/index'>Logout</a>")
else:
    print("<h1>Welcome to Simple Bank</h1>")
    print("<p>You are not logged in.</p>")

    print("<h2>Login</h2>")
    print("<form method='POST' action='http://localhost:8081/login?return_to=http://localhost:8080/dashboard'>")
    print("Username: <input type='text' name='username'><br>")
    print("Password: <input type='password' name='password'><br>")
    print("<input type='submit' value='Login'>")
    print("</form>")

    print("<h2>New user? Sign up</h2>")
    print("<form method='POST' action='http://localhost:8081/signup?return_to=http://localhost:8080/dashboard'>")
    print("Username: <input type='text' name='username'><br>")
    print("Password: <input type='password' name='password'><br>")
    print("<input type='submit' value='Sign Up'>")
    print("</form>")

print("</body>")
print("</html>")



