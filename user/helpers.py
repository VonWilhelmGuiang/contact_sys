def user_logged_in(session):
    if ('user_logged_in' in session) and ('user_id' in session):
        return True
    else:
        return False
