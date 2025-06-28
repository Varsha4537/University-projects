# 🏦 CGI Bank System

This is a lightweight bank web application built using raw Python CGI scripts and a custom socket-based HTTP server. It features user authentication, session management with cookies, and the ability to manage account balances (add/remove funds).

## 🚀 Features

- 🔐 User Login and Logout: I have a seperate login_server.py that handles login, signup and logout requestes. There is a users.json file and sessions.json file that keep track of user information and session information. All the files are inside cgi-bin for ease of use.
- 🍪 Session Management using Cookies: On successful login, a session ID is generated and stored in sessions.json with the corresponding username. The session is stored in the user's browser as a cookie: session=<uuid>. On logout: The specific session ID is removed from sessions.json, the cookie is expired using Set-Cookie: session=; Max-Age=0, Other users' sessions are unaffected.
- 💰 Add and Remove Money: Each user has a `balance_username.py` file that is stored inside cgi-bin.
- 🧾 Individual User Balances (stored in separate files): I have created a seperate folder called balances inside cgi-bi that stores all uses balances. Amount is sent via POST, and balance is updated accordingly.
- 👤 Sessions stored in `sessions.json` with support for multiple users

## 🔁 Routing
- To simplify clean URLs like `/dashboard`, we use a `routes.json` file:
- The server reads this file and maps friendly URLs to actual Python scripts in cgi-bin/.

```json
{
  "/dashboard": "/dashboard.py",
  "/index": "/index.py"
}

NOTES:
http://localhost:8080/index   ---> this works, so please go directly to this link
http://localhost:8080   ---> But this doesn't work due to the route mapping

## 🔁 Routing

The server logs every HTTP request in access.log using the Common Log Format:

host - user [timestamp] "request" status bytes

127.0.0.1 - - [10/Apr/2025:14:32:10 +0000] "GET /index HTTP/1.1" 200 512

This helps with debugging, monitoring, and tracking user activity.

## NOTE
This program was compiled on a mac, and may require some tweaks when run on windows or linux accordingly.