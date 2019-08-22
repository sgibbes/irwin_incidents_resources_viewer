
import json
import requests
import urllib2
import urllib

# sample code to query IRWIN incidents API. You will need your IRWIN username/password.


def query_api(url, token, where):

    statsdata = urllib.urlencode({'f': 'json',
                                  'token': token,
                                  'where': where,
                                  'outFields': '*'})

    # # get the response
    req = urllib2.Request(url)
    req.add_header('Referer', 'local')

    statres = urllib2.urlopen(url=req, data=statsdata)
    statsfjstr = statres.read()

    # load to json
    return json.loads(statsfjstr)


def get_token(url, usr, pswd):

    r = requests.post(url,
                      data={"username": usr,
                            "password": pswd,
                            'f': 'json'})

    response = r.json()

    return response['token']


def load_response(api_response):

    feature_coll = {'features': []}

    feature_coll['features'].extend(api_response['features'])

    return feature_coll['features']


# set up your username/password
usrname = 'your_username'
pswd = 'your_password'

# the url where you get your token
token_url = 'https://irwin.doi.gov/arcgis/tokens/generateToken?'

# get token
token = get_token(token_url, usrname, pswd)

# the incidents api endpoint
endpoint_url = 'https://irwin.doi.gov/arcgis/rest/services/Irwin/FeatureServer/0/query'

# set up a where clause. If nothing specified, set it to 1=1. Strings must be wrapped in single quotes
where = "IrwinID = '{5C430B3C-327B-493D-9AD0-FD27897F1064}'"

api_response = query_api(endpoint_url, token, where)

print load_response(api_response)
