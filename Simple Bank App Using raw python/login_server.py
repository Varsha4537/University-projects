import socket
import os
import subprocess
import inspect
import json
import uuid
from datetime import datetime

HOST = 'localhost'
PORT = 8081
DOCROOT = './cgi-bin'
SESSIONS_FILE = os.path.join(DOCROOT, "sessions.json")
ROUTES_FILE = "routes.json"
LOGFILE = "access.log"

def load_routes():
    try:
        with open(ROUTES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def log_request(client_addr, request_line, status_code, response_size, username="-"):
    now = datetime.now()
    log_time = now.strftime('%d/%b/%Y:%H:%M:%S %z')
    host = client_addr[0]

    # Build log line in Common Log Format
    log_entry = f'{host} - {username} [{log_time}] "{request_line}" {status_code} {response_size}\n'

    with open(LOGFILE, "a") as f:
        f.write(log_entry)

def load_sessions():
    if not os.path.exists(SESSIONS_FILE):
        return {}
    with open(SESSIONS_FILE, 'r') as f:
        return json.load(f)

def save_sessions(sessions):
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(sessions, f)

def parse_request(data):
    print(f"{inspect.currentframe().f_lineno}: Parsing request data")
    lines = data.split('\r\n')
    request_line = lines[0]
    headers = {}
    for line in lines[1:]:
        if ': ' in line:
            k, v = line.split(': ', 1)
            headers[k] = v
    print(f"{inspect.currentframe().f_lineno}: Parsed request line: {request_line}")
    return request_line, headers

def run_cgi(script_path, query, env, body=""):
    print(f"{inspect.currentframe().f_lineno}: Running CGI script at {script_path}")
    env_vars = os.environ.copy()
    env_vars.update(env)
    env_vars['QUERY_STRING'] = query or ''
    env_vars['CONTENT_LENGTH'] = str(len(body))

    proc = subprocess.Popen(
        ['python3', script_path],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        env=env_vars
    )
    output, _ = proc.communicate(input=body.encode())
    print(f"{inspect.currentframe().f_lineno}: CGI script output: {output}")
    return output.decode()

def extract_username(output):
    for line in output.splitlines():
        if line.startswith("X-Username:"):
            return line.split(":", 1)[1].strip()
    return None

def parse_cgi_output(output):
    headers, _, body = output.partition("\n\n")
    if not headers.startswith("Status:") and "Content-Type" not in headers:
        headers = "Content-Type: text/html\n" + headers
    if "Status: 302 Found" in headers:
        headers = headers.replace("Status: 302 Found", "HTTP/1.1 302 Found")
    else:
        headers = "HTTP/1.1 200 OK\r\n" + headers
    return headers.replace("\n", "\r\n") + "\r\n\r\n" + body

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"{inspect.currentframe().f_lineno}: Login Server running on http://{HOST}:{PORT}")

    routes = load_routes()

    while True:
        print(f"{inspect.currentframe().f_lineno}: Waiting for a connection")
        conn, addr = s.accept()
        with conn:
            print(f"{inspect.currentframe().f_lineno}: Connection from {addr}")
            data = conn.recv(4096).decode()
            if not data:
                print(f"{inspect.currentframe().f_lineno}: No data received, closing connection")
                continue

            request_line, headers = parse_request(data)
            method, path, _ = request_line.split()
            script, _, query = path.partition('?')

            # Route mapping
            mapped_script = routes.get(script, script)
            script_path = os.path.normpath(os.path.join(DOCROOT, mapped_script.lstrip('/')))

            if os.path.isfile(script_path):
                env = {
                    'REQUEST_METHOD': method,
                    'HTTP_COOKIE': headers.get('Cookie', ''),
                }

                body = ""
                if method == "POST":
                    body_split = data.split("\r\n\r\n", 1)
                    if len(body_split) == 2:
                        body = body_split[1]

                raw_output = run_cgi(script_path, query, env, body)
                username = extract_username(raw_output)

                if username:
                    session_id = str(uuid.uuid4())
                    sessions = load_sessions()
                    sessions[session_id] = username
                    save_sessions(sessions)

                    # Inject cookie and redirect
                    http_response = (
                        "HTTP/1.1 302 Found\r\n"
                        f"Set-Cookie: session={session_id}; Path=/\r\n"
                        "Location: /dashboard\r\n"
                        "Content-Type: text/html\r\n\r\n"
                        "Redirecting..."
                    )
                    conn.sendall(http_response.encode())
                    log_request(addr, request_line, 200, len(http_response), username or "-")

                else:
                    http_response = parse_cgi_output(raw_output)
                    conn.sendall(http_response.encode())
                    log_request(addr, request_line, 200, len(http_response), username or "-")

            else:
                conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n404 Not Found")
                log_request(addr, request_line, 404, len(http_response))

            print(f"{inspect.currentframe().f_lineno}: Closing connection")


