import requests
import string
import json
import urllib
import urllib2
import sys
import pandas as pd


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


def get_capability(list_of_features, token, capability_coll):
    url = 'https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services' \
                   '/[OAT_NEXT]_Resources_VIEW_(Read_Only)/FeatureServer/2/query'
    for record in list_of_features:
        irwin_rid = record['attributes']['IrwinRID']

        where = "IrwinRID = '{}'".format(irwin_rid.upper())

        list_of_capabilities = query_api(url, token, where)

        capability_coll['features'].extend(list_of_capabilities['features'])

    return capability_coll

