import ConfigParser
import requests


# some constants

CONFIG_PATH = "test.ini"

REQ_USER_AGENT = "libreshelf"
REQ_HEADERS = {
    "User-Agent": REQ_USER_AGENT
}

BC_BASE_URL = "https://bandcamp.com"

# /constants


def bcLogin(user, passwd):
    session = requests.Session()

    params = {
        "user.name": user,
        "login.password": passwd
    }
    req = session.post(BC_BASE_URL + "/login_cb", params=params, headers=REQ_HEADERS)

    response = req.json()

    if response["ok"] == True:
        return session
    else:
        return False

# untested
def bcLogout(session):
    return session.get(BC_BASE_URL + "/logout", headers=REQ_HEADERS)



# get ref to config file
cfg = ConfigParser.RawConfigParser()
cfg.read(CONFIG_PATH)


bcUser = cfg.get("bandcamp", "user")
bcPasswd = cfg.get("bandcamp", "passwd")

bcSession = bcLogin(bcUser, bcPasswd)

if bcSession == False:
    print "Failed to login to Bandcamp"
    sys.exit(1)

with bcSession:
    print bcLogout(bcSession).text.encode('utf8')
