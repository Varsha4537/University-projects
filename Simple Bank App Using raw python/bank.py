import socket
import os
import subprocess
import inspect
from datetime import datetime


import json

def load_routes():
    try:
        with open("routes.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
HOST = 'localhost'
PORT = 8080
DOCROOT = './cgi-bin'
LOGFILE = "access.log"


def log_request(client_addr, request_line, status_code, response_size, username="-"):
    now = datetime.now()
    log_time = now.strftime('%d/%b/%Y:%H:%M:%S %z')
    host = client_addr[0]

    # Build log line in Common Log Format
    log_entry = f'{host} - {username} [{log_time}] "{request_line}" {status_code} {response_size}\n'

    with open(LOGFILE, "a") as f:
        f.write(log_entry)

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

def run_cgi(script_path, method, query, env, post_data=''):
    print(f"{inspect.currentframe().f_lineno}: Running CGI script at {script_path}")
    env_vars = os.environ.copy()
    env_vars.update(env)
    env_vars['REQUEST_METHOD'] = method
    if method == 'GET':
        env_vars['QUERY_STRING'] = query
    elif method == 'POST':
        env_vars['CONTENT_LENGTH'] = str(len(post_data))

    proc = subprocess.Popen(['python3', script_path],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            env=env_vars)
    output, _ = proc.communicate(input=post_data.encode())
    print(f"{inspect.currentframe().f_lineno}: CGI script output: {output}")
    return output

# Setup socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
print(f"{inspect.currentframe().f_lineno}: Bank CGI Server on http://{HOST}:{PORT}")

while True:
    print(f"{inspect.currentframe().f_lineno}: Waiting for a connection")
    conn, addr = s.accept()
    print(f"{inspect.currentframe().f_lineno}: Connection from {addr}")
    data = conn.recv(4096).decode()
    if not data:
        print(f"{inspect.currentframe().f_lineno}: No data received, closing connection")
        conn.close()
        continue

    request_line, headers = parse_request(data)
    parts = data.split('\r\n\r\n', 1)
    body = parts[1] if len(parts) > 1 else ''

    try:
        method, path, _ = request_line.split()
    except ValueError:
        conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\nBad Request")
        conn.close()
        continue

    script, _, query = path.partition('?')

    if script == "/":
        script = "/index.py"

    # Map clean path using routes config
    ROUTES = load_routes()
    mapped_script = ROUTES.get(script)
    if mapped_script:
        script_path = os.path.normpath(os.path.join(DOCROOT, mapped_script.lstrip('/')))
    else:
        # If not mapped, assume full path is already correct
        script_path = os.path.normpath(os.path.join('.', script.lstrip('/')))


    print(f"{inspect.currentframe().f_lineno}: m:{method}, p:{path}, q:{query}, s:{script_path}, b:{body}")

    if os.path.isfile(script_path):

        env = {'HTTP_COOKIE': headers.get('Cookie', '')}
        response = run_cgi(script_path, method, query, env, post_data=body)

        # Decode the response to parse headers/body
        response_str = response.decode()

        # Separate headers and body
        cgi_headers, _, response_body = response_str.partition("\n\n")

        # Fallback if neither Status nor Content-Type are in the headers
        if not cgi_headers.startswith("Status:") and "Content-Type" not in cgi_headers:
            cgi_headers = "Content-Type: text/html\n" + cgi_headers

        # Replace or prepend appropriate status line
        if "Status: 302 Found" in cgi_headers:
            status_code = 302
            cgi_headers = cgi_headers.replace("Status: 302 Found", "HTTP/1.1 302 Found")
        else:
            status_code = 200
            cgi_headers = "HTTP/1.1 200 OK\r\n" + cgi_headers

        # Ensure proper HTTP line endings
        http_response = cgi_headers.replace("\n", "\r\n") + "\r\n\r\n" + response_body

        # Send the response
        conn.sendall(http_response.encode())
        log_request(addr, request_line, status_code, len(http_response))


    else:
        print(f"{inspect.currentframe().f_lineno}: Script not found at {script_path}")
        conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n404 Not Found")
        log_request(addr, request_line, 404, len(http_response))

    print(f"{inspect.currentframe().f_lineno}: Closing connection")
    conn.close()

