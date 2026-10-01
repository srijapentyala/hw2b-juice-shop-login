# Juice Shop-style login form

A small login page modeled on the OWASP Juice Shop login screen. It is the front-end piece of a web-security homework assignment. The page asks for an email and a password, checks them in the browser, and sends them to a Python server that checks them again.

## What it checks

Both the browser and the server reject the login when:

- the email or the password is empty
- the email does not contain `@`
- the password is shorter than 8 characters

The server stores only a PBKDF2 hash of the demo password. It compares that hash in constant time. User input is never placed into a SQL string. The page shows the submitted email on the result line.

## Run it

Python 3.11 or newer is enough. There are no packages to install.

```bash
python3 server.py
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080).

Demo account: `demo@juice-sh.op` / `JuiceShop1`

## Layout

- `index.html` is the login page
- `login.js` is the client-side check and the submit handler
- `styles.css` is the page layout
- `server.py` repeats the checks and verifies the password hash
