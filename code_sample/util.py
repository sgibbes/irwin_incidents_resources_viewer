import requests
import json
import urllib
import urllib2
import pandas as pd
import csv


def min_max_objid(stats_json):
    seq = [x['attributes']['OBJECTID'] for x in stats_json['features']]

    return min(seq), max(seq)


def get_token(usr, pswd):
    # get a token in order to query the endpoint
    token_url = 'https://www.arcgis.com/sharing/generatetoken?expiration=120&' \
                'referer=localhost&f=json&username={}&password={}'.format(usr, pswd)
    r = requests.post(token_url,
                      data={"username": usr,
                            "password": pswd,
                            'f': 'json'})

    response = r.json()

    return response['token']


def query_api(url, token, where):

    statsdata = urllib.urlencode({'f': 'json',
                                  'token': token,
                                  'where': where,
                                  'outFields': '*'
                                  })

    # # get the response
    req = urllib2.Request(url)
    req.add_header('Referer', 'local')

    statres = urllib2.urlopen(url=req, data=statsdata)
    statsfjstr = statres.read()

    return json.loads(statsfjstr)


def response_to_dict(feature_coll, csv_file):
    # put attributes into dictionary
    attributes = []
    for f in feature_coll['features']:

        try:
            # add geometry to the attributes as a new key
            f['attributes']['geometry'] = f['geometry']

        except:
            pass

        attributes.append(f['attributes'])

    df = pd.DataFrame(attributes)
    df.to_csv(csv_file)


def response_to_dict_nopd(feature_coll, csv_file):
    # put attributes into dictionary
    attributes = []
    for f in feature_coll['features']:

        try:
            # add geometry to the attributes as a new key
            f['attributes']['geometry'] = f['geometry']

        except:
            pass

        attributes.append(f['attributes'])

    csv_columns = attributes[0].keys()

    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in attributes:
                writer.writerow(data)
    except IOError:
        print("I/O error")



