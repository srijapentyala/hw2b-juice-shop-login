# Juice Shop-style login form

Course CSCE 703. UIN 937006978. Email srijapentyala@tamu.edu.

A login page built in the shape of [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/): an email, a password, and a Log in button. The browser checks the fields first. A small Python server checks them again and compares the password with a stored hash.

This is the front end for a web-security assignment. It is deliberately small so the checks, the password comparison, and one unsafe display of the email are easy to follow.

## Run

Python 3.11 or newer. Nothing to install.

```bash
python3 server.py
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080). The process binds to localhost only. Ctrl+C stops it.

Sign in with `demo@juice-sh.op` / `JuiceShop1`. A match prints **Logged in.** in green. Any other pair that is well formed prints **Invalid email or password.** An unknown account and a wrong password get the same sentence, so the form does not reveal which one failed.

## What happens on Log in

1. `login.js` refuses an empty email or password, an email without a real `@`, and a password shorter than 8 characters. Those errors never leave the browser.
2. Anything that passes is sent as JSON to `POST /login`.
3. `server.py` repeats the same three checks. A bad format is HTTP 400. A format that is fine but does not match the demo account is HTTP 401.
4. The status line is set as text. The line under it is the email the browser sent, written with `innerHTML`.

There is no database. The email and password are never pasted into a query.

## Password check

The demo password does not appear as a string next to the comparison. `server.py` stores a salt and a PBKDF2-HMAC-SHA256 hash (200,000 rounds) and checks the attempt with `hmac.compare_digest`, so the comparison does not stop at the first differing byte.

## The result line

The status text is safe. The submitted email is not: `login.js` assigns it with `innerHTML`, so markup in the email is parsed as HTML. That is the weakness the write-up exploits.

The repair is to assign that line with `textContent`, and to send `Content-Security-Policy: script-src 'self'` so an inline handler cannot run even if a later change inserts one.

## Write-up

[HW2B-OWASP-Juice-Shop.pdf](submission/HW2B-OWASP-Juice-Shop.pdf) is the homework document: the Juice Shop findings, this form, and the attack notes. The screenshots in that PDF are in [`submission/`](submission/).

## Files

| File | What it owns |
| --- | --- |
| `index.html` | The form |
| `login.js` | The browser checks and the submit handler |
| `styles.css` | Layout |
| `server.py` | The pages, the repeated checks, and the hash comparison |
