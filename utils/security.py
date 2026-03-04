import time

MAX_ATTEMPTS = 5
BLOCK_TIME = 300

login_attempts = {}


def check_block(ip):

    if ip not in login_attempts:
        return False

    data = login_attempts[ip]

    if time.time() < data["blocked_until"]:
        return True

    return False


def register_attempt(ip):

    if ip not in login_attempts:
        login_attempts[ip] = {
            "attempts": 0,
            "blocked_until": 0
        }

    data = login_attempts[ip]
    data["attempts"] += 1

    if data["attempts"] >= MAX_ATTEMPTS:

        data["blocked_until"] = time.time() + BLOCK_TIME
        data["attempts"] = 0
        return 0

    remaining = MAX_ATTEMPTS - data["attempts"]

    return remaining


def reset_attempt(ip):

    login_attempts[ip] = {
        "attempts": 0,
        "blocked_until": 0
    }