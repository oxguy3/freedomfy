import ConfigParser
import requests
import json
import pprint


# some constants

CONFIG_PATH = "test.ini"

REQ_USER_AGENT = "libreshelf"
REQ_BASE_HEADERS = {
    "User-Agent": REQ_USER_AGENT
}

BC_BASE_URL = "https://bandcamp.com"

# /constants

# creates a requests session and logs in to a Bandcamp account
# returns session with necessary cookies if successful; else returns False
def bcStartSession(user, passwd):
    session = requests.Session()
    session.headers.update(REQ_BASE_HEADERS)
    return bcLogin(session, user, passwd)

# logs in to a Bandcamp account with a given session
# for most cases, call bcStartSession() instead of this method
# returns session with necessary cookies if successful; else returns False
def bcLogin(session, user, passwd):
    params = {
        "user.name": user,
        "login.password": passwd
    }
    req = session.post(BC_BASE_URL + "/login_cb", params=params)

    response = req.json()

    if response["ok"] == True:
        return session
    else:
        return False

# (UNTESTED METHOD) logs out of a Bandcamp account
def bcLogout(session):
    return session.get(BC_BASE_URL + "/logout")

# retrieves useful info from Bandcamp profile
# session must be logged in as the given user
def bcGetProfileData(session, user):
    req = session.get(BC_BASE_URL + "/" + user)

    purchasesPrefix = "    item_lookup: "
    collectionPrefix = "    item_details: "
    redownloadsPrefix = "    redownload_urls: "

    purchases = None
    collection = None
    redownloads = None

    lines = req.text.splitlines()

    for line in lines:

        if line.startswith(purchasesPrefix):
            purchasesJson = line[len(purchasesPrefix):].rstrip(",")
            purchases = json.loads(purchasesJson)

        if line.startswith(collectionPrefix):
            collectionJson = line[len(collectionPrefix):].rstrip(",")
            collection = json.loads(collectionJson)

        if line.startswith(redownloadsPrefix):
            redownloadsJson = line[len(redownloadsPrefix):].rstrip(",")
            redownloads = json.loads(redownloadsJson)

    assert purchases != None
    assert collection != None
    assert redownloads != None

    entities = []

    for redownload in redownloads.items():
        saleItemId = redownload[0][1:]

        theDict = {}
        downloadUrl = redownload[1]
        isSaleItemMatched = False

        for item in collection.values():
            if str(item["sale_item_id"]) == saleItemId:
                theDict["type"] = item["item_type"]
                theDict["title"] = item["item_title"]
                theDict["artist"] = item["band_name"]
                theDict["infoUrl"] = item["item_url"]
                theDict["numTracks"] = item["num_streamable_tracks"]
                theDict["artId"] = str(item["item_art_id"]).rjust(10, "0") # url: https://f1.bcbits.com/img/a<ARTID>_1.jpg
                isSaleItemMatched = True
                break

        assert isSaleItemMatched

        dlReq = session.get(downloadUrl)

        dlItemsPrefix = "    items: "
        dlItems = None

        dlLines = dlReq.text.splitlines()
        for dlLine in dlLines:
            if dlLine.startswith(dlItemsPrefix):
                dlItemsJson = dlLine[len(dlItemsPrefix):].rstrip(",")
                dlItems = json.loads(dlItemsJson)
                break

        assert dlItems != None
        assert len(dlItems) == 1

        dlDataMp3 = dlItems[0]["downloads"]["mp3-v0"]
        theDict["mp3Url"] = dlDataMp3["url"]
        theDict["mp3Size"] = dlDataMp3["size_mb"]

        entities.append(theDict)

    pprint.pprint(entities)



# get ref to config file
cfg = ConfigParser.RawConfigParser()
cfg.read(CONFIG_PATH)


bcUser = cfg.get("bandcamp", "user")
bcPasswd = cfg.get("bandcamp", "passwd")

bcSession = bcStartSession(bcUser, bcPasswd)

if bcSession == False:
    print "Failed to login to Bandcamp"
    sys.exit(1)

with bcSession:
    #print bcLogout(bcSession).text.encode('utf8')

    bcGetProfileData(bcSession, bcUser)
