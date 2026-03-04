def check_login(username, password, ADMIN_USER, ADMIN_PASS):

    if username == ADMIN_USER and password == ADMIN_PASS:
        return True

    return False