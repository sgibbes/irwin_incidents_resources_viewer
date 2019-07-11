import json
import requests
import urllib2, urllib
import pprint
import sys


def query_api(i, token, where):

    # outfields = 'FireDiscoveryDateTime, IrwinID, IsValid, ConflictParentIrwinID,  ' \
    #             'ModifiedOnDateTime,  OBJECTID, CreatedBySystem, CreatedOnDateTime, ' \
    #             'DispatchCenterID, IsQuarantined, ControlDateTime, ContainmentDateTime, ' \
    #             'ModifiedBySystem, InitialResponseDateTime, FireOutDateTime'

    # outfields = 'IrwinID, FireDiscoveryDateTime, IsValid, CreatedOnDateTime, DispatchCenterID'
    if i.url_type == 'resource':
        outfields = '*'
    else:
        outfields = 'IrwinRID'

    statsdata = urllib.urlencode({'f': 'json',
                                  'token': token,
                                  'where': where,
                                  'outFields': outfields})

    # # get the response
    req = urllib2.Request(i.url)
    req.add_header('Referer', 'local')

    statres = urllib2.urlopen(url=req, data=statsdata)
    statsfjstr = statres.read()

    # load to json
    return json.loads(statsfjstr)


def load_response(response):

    feature_coll = {'features': []}

    feature_coll['features'].extend(response['features'])

    # pprint.pprint(feature_coll['features'])

    return feature_coll['features']


def get_token(url, usr, pswd):

    r = requests.post(url,
                      data={"username": usr,
                            "password": pswd,
                            'f': 'json'})

    response = r.json()

    return response['token']


def where_inputs(i):

    # set up at least one where clause that can be added onto
    where = "CreatedOnDateTime > 0"

    # these are all possible where clauses to build
    if i.url_type == 'resource':
        var_list = [i.id, 'CreatedBySystem']
    else:
        var_list = [i.id, 'PooState']

    # for each of the variables, ask for input. press enter to skip that one
    inputs_dict = {}
    for var in var_list:
        inputs_dict[var] = raw_input("{}: ".format(var))

    for name, val in inputs_dict.iteritems():
        if val is not '':
            # lowercase the irwin id
            if name == i.id:
                val = val.lower()
            # add the where clause to build where statement
            where += " AND {} = '{}'".format(name, val)

    return where
