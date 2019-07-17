import json
import urllib2, urllib
from random import randrange, randint
import names


class ResourceAttributes:

    def __init__(self):

        self.firstname = None
        self.lastname = None
        self.middlename = None
        self.birthmonthday = None

        self.providerunit = None
        self.homedispatchunit = None
        self.resourcesor = None
        self.home_unit = None


def feature(a):

    phone = "{}-{}-{}".format(randint(100, 999), randint(100, 999), randint(1000, 9999))

    json_features = {
            "attributes": {
                "BirthMonthDay": a.birthmonthday,
                "CurrentDispatchUnit": a.homedispatchunit,
                "EmploymentCategoryCode": "Career",
                "HomeDispatchUnit": a.homedispatchunit,
                "GeneralStatus": "Available",
                "IsActive": 1,
                "IsLocationTrackingEnabled": 0,
                "JetPort": "ONT",
                "ResourceKind": "Overhead",
                "ProviderUnit": a.homedispatchunit,
                "HomeUnit": a.home_unit,
                "NameFirst": a.firstname,
                "NameMiddle": a.middlename,
                "NameLast": a.lastname,
                "PrimaryEmail": "moonwalker1@nasa.gov",
                "PrimaryPhone": phone,
                "ResourceSOR": a.resourcesor,
                "ManagerContactInfo": "John Doe WAWAS Training Manager, 360-777-2316"
            },
            "geometry": {
                "x": -117.985835,
                "y": 34.259355
            }
        }

    return json_features


def pad_zeros(data):
    if len(str(data)) == 1:
        return "0{}".format(data)

    else:
        return data


def construct_monthday():

    month = pad_zeros(randrange(1, 13))
    day = pad_zeros(randrange(1, 29))

    return "{}{}".format(month, day)


def construct_add(home_dispatch_unit, resourcesor):

    attributes = ResourceAttributes()

    attributes.firstname = names.get_first_name()
    attributes.lastname = names.get_last_name()
    attributes.middlename = names.get_first_name()
    attributes.birthmonthday = construct_monthday()

    attributes.homedispatchunit = home_dispatch_unit
    attributes.resourcesor = resourcesor

    attributes.home_unit = unit_ids(home_dispatch_unit)
    return attributes


def create_many_resources(num, home_dispatch_unit, resourcesor):
    json_feature_list = []
    for i in range(0, num):
        attributes = construct_add(home_dispatch_unit, resourcesor)

        json_feature = feature(attributes)

        json_feature_list.append(json_feature)

    return json_feature_list


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


def unit_ids(dispatch_center):
    d = {'AKYTDC': 'AKUYD', 'AKFASC': None, 'TXTIC': 'TXTXF', 'CAANCC': 'CAANF', 'CASBCC': 'CABDF', 'CALACC': None}

    return d[dispatch_center]