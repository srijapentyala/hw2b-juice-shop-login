#!/usr/bin/env python3
"""Login server for the Juice Shop-style form.

Checks are repeated on the server. The email and password are never
concatenated into a query.
"""

import hashlib
import hmac
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8080
ROOT = Path(__file__).resolve().parent
FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/login.js": ("login.js", "text/javascript; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
}

# Demo account. The password is not stored. Only a PBKDF2-HMAC-SHA256
# hash and its salt are kept. A production app should use bcrypt or Argon2.
DEMO_EMAIL = "demo@juice-sh.op"
DEMO_SALT = bytes.fromhex("4f6a7c2e91ab45d08c13e6f0a2b94715")
DEMO_HASH = bytes.fromhex(
    "22570be273b7bed76469ba0ccbf0c7096c163e79af948889821af84d92fcfb44"
)
PBKDF2_ROUNDS = 200_000


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ROUNDS
    )


def validate(email, password):
    if not isinstance(email, str) or not isinstance(password, str):
        return "Email and password are required."
    email = email.strip()
    if email == "" or password == "":
        return "Email and password are required."
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        return "Email must contain @."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    return None


class LoginHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        spec = FILES.get(self.path.split("?", 1)[0])
        if spec is None:
            self.send_error(404)
            return
        name, content_type = spec
        body = (ROOT / name).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none'",
        )
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path.split("?", 1)[0] != "/login":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        if length > 4096:
            self._json(413, {"ok": False, "message": "Request is too large."})
            return
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json(400, {"ok": False, "message": "Request must be JSON."})
            return

        email = payload.get("email", "")
        password = payload.get("password", "")
        error = validate(email, password)
        if error:
            self._json(400, {"ok": False, "message": error})
            return

        email = email.strip()
        candidate = hash_password(password, DEMO_SALT)
        if hmac.compare_digest(email.lower(), DEMO_EMAIL) and hmac.compare_digest(
            candidate, DEMO_HASH
        ):
            self._json(200, {"ok": True, "message": "Logged in."})
            return
        self._json(401, {"ok": False, "message": "Invalid email or password."})

    def _json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        return


def main():
    server = ThreadingHTTPServer((HOST, PORT), LoginHandler)
    print(f"Login form at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
