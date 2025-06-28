import http.client
import urllib.parse
from urllib.parse import urljoin

class MiniCurl:
    def __init__(self):
        self.cookies = {}

    def _parse_set_cookie(self, headers):
        for header in headers:
            if header[0].lower() == 'set-cookie':
                cookie_parts = header[1].split(';')
                for part in cookie_parts:
                    if '=' in part:
                        k, v = part.strip().split('=', 1)
                        self.cookies[k] = v

    def _format_cookie_header(self):
        return '; '.join(f"{k}={v}" for k, v in self.cookies.items())

    def request(self, url, method='GET', data=None, follow_redirects=True):
        parsed_url = urllib.parse.urlparse(url)
        conn = http.client.HTTPConnection(parsed_url.hostname, parsed_url.port or 80)

        path = parsed_url.path or '/'
        if parsed_url.query and method == 'GET':
            path += '?' + parsed_url.query

        headers = {}
        if self.cookies:
            headers['Cookie'] = self._format_cookie_header()

        body = None
        if method == 'POST' and data:
            body = urllib.parse.urlencode(data)
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Content-Length'] = str(len(body))

        conn.request(method, path, body=body, headers=headers)
        response = conn.getresponse()

        self._parse_set_cookie(response.getheaders())

        print(f"\n➡️ {method} {url}")
        print(f"⬅️ {response.status} {response.reason}")
        for header in response.getheaders():
            print(f"{header[0]}: {header[1]}")
        print("\n📄 Response:\n" + response.read().decode())

        if follow_redirects and response.status in (301, 302):
            location = dict(response.getheaders()).get('Location')
            if location:
                # Combine base URL with relative redirect path
                redirect_url = urljoin(url, location)
                print(f"\n🔁 Redirecting to {location}...\n")
                conn.close()
                return self.request(redirect_url, method='GET', follow_redirects=follow_redirects)

        conn.close()


def interactive_curl():
    curl = MiniCurl()
    while True:
        print("\n🌐 === Mini Curl ===")
        url = input("Enter URL (or 'exit' to quit): ").strip()
        if url.lower() == 'exit':
            break

        method = input("Method [GET/POST] (default: GET): ").strip().upper()
        if method not in ['GET', 'POST']:
            method = 'GET'

        data = {}
        if method == 'POST':
            while True:
                kv = input("Enter POST data key=value (or blank to finish): ").strip()
                if not kv:
                    break
                if '=' in kv:
                    k, v = kv.split('=', 1)
                    data[k] = v

        curl.request(url, method=method, data=data)

if __name__ == "__main__":
    interactive_curl()
