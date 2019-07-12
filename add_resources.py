import json
import requests
import urllib2, urllib
import query
import pprint
import sys


# generate different resource and send to irwin test environment as new features

def query_api(url, token, json_features):

    statsdata = urllib.urlencode({'f': 'json',
                                  'token': token,
                                  'features': json_features})


    # # get the response
    req = urllib2.Request(url)
    req.add_header('Referer', 'local')

    statres = urllib2.urlopen(url=req, data=statsdata)
    statsfjstr = statres.read()

    # load to json
    return json.loads(statsfjstr)

# Log in as qualification_test
token_url = 'https://irwint.doi.gov/arcgis/tokens/generateToken?'

token = query.get_token(token_url, 'qualification_test', 'Testing!Testing!123')

url = 'https://irwint.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/0/addFeatures'

json_features = {
"attributes": {
"BirthMonthDay":"0807",
"CurrentDispatchUnit":"CABDU",
"EmploymentCategoryCode":"Career",
"HomeDispatchUnit":"CABDCD",
"GeneralStatus":"Available",
"IsActive":1,
"IsLocationTrackingEnabled":0,
"JetPort":"ONT",
"ResourceKind":"Overhead",
"ProviderUnit":"CABDU",
"HomeUnit":"CABDU",
"NameFirst":"Neil",
"NameMiddle":"Aldens",
"NameLast":"Armstrongs",
"PrimaryEmail":"moonwalker1@nasa.gov",
"PrimaryPhone":"222-123-9876",
"ResourceSOR":"iqcs",
"ManagerContactInfo": "John Doe WAWAS Training Manager, 360-777-2316"
},
"geometry":{
"x": -117.985835,
"y": 34.259355
}
}

print query_api(url, token, json_features)