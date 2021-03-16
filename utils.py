import bcrypt
from main import session


def hash_password(psw):
    return bcrypt.hashpw(psw.encode(), bcrypt.gensalt())

def check_password(psw, hash):
    return bcrypt.checkpw(psw.encode(), hash)


def cursor_to_list(cursor, filter=None):
    if filter is None:
        a = []
        for i in cursor:
            a.append(i)
        return a
    else:
        a = []
        for i in cursor:
            a.append(i[filter])
        return a


def check_if_logged():
    try:
        session["logged"]
    except KeyError:
        return False
    else:
        if session["logged"]:
            return True
        else:
            return False
