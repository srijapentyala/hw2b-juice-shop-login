# Juice Shop-style login form

A small login page modeled on the OWASP Juice Shop login screen. It is the front-end piece of a web-security homework assignment. The page asks for an email and a password, checks them in the browser, and sends them to a Python server that checks them again.

There is no database. Nothing the user types is concatenated into a SQL string.

## Requirements

Python 3.11 or newer. No packages to install.

## Run it

From this directory:

```bash
python3 server.py
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080). The server listens on `127.0.0.1` only. Stop it with Ctrl+C.

## Demo account

| Email | Password |
| --- | --- |
| `demo@juice-sh.op` | `JuiceShop1` |

A correct login shows **Logged in.** in green. Any other email and password that pass the format checks show **Invalid email or password.** The server answers with the same message for an unknown email and a wrong password.

The demo password is not stored in the source. `server.py` keeps a PBKDF2-HMAC-SHA256 hash and a salt, and compares the candidate with `hmac.compare_digest`.

## What it checks

`login.js` rejects the form before it is sent when:

- the email or the password is empty
- the email does not contain `@`, or `@` is the first or last character
- the password is shorter than 8 characters

`server.py` repeats those three checks on `POST /login`. A request that fails them gets HTTP 400. A request that passes them but does not match the demo account gets HTTP 401.

## What the page shows

After a request reaches the server, the status line is plain text. The line under it is the submitted email, inserted with `innerHTML` in `login.js`. That is the behavior exercised in the homework write-up.

## Files

| File | Role |
| --- | --- |
| `index.html` | Login form: email, password, and the Log in button |
| `login.js` | Client-side checks and the submit handler |
| `styles.css` | Page layout |
| `server.py` | Static files, the repeated checks, and the password comparison |
