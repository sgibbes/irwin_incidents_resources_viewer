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
        self.jet_port = 'ONT'
        self.resource_clearinghouse_id = None
        self.resource_kind = None
        self.manager_contact_info = None
        self.primary_email = "#"


def capability_type(irwin_ctid, irwin_rid):
    json_feature = {
        "attributes": {
        "Capacity": 'Qualified',

        'IrwinCTID': irwin_ctid,
        'IrwinRID': irwin_rid

        }}

    return json_feature


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
                "JetPort": a.jet_port,
                "ResourceKind": a.resource_kind,
                "ProviderUnit": a.home_unit,
                "HomeUnit": a.home_unit,
                "NameFirst": a.firstname,
                "NameMiddle": a.middlename,
                "NameLast": a.lastname,
                "PrimaryEmail": "moonwalker1@nasa.gov",
                "PrimaryPhone": phone,
                "ResourceSOR": a.resourcesor,
                "ManagerContactInfo": a.manager_contact_info,
                "ResourceClearinghouseID": a.resource_clearinghouse_id
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


def construct_oh(home_dispatch_unit, resourcesor):

    attributes = ResourceAttributes()

    attributes.resource_kind = "Overhead"
    attributes.firstname = names.get_first_name()
    attributes.lastname = names.get_last_name()
    attributes.middlename = names.get_first_name()
    attributes.birthmonthday = construct_monthday()

    attributes.homedispatchunit = home_dispatch_unit
    attributes.resourcesor = resourcesor

    attributes.home_unit = unit_ids(home_dispatch_unit)
    attributes.resource_clearinghouse_id = "#"
    return attributes


def create_many_resources(num, home_dispatch_unit, resourcesor):
    json_feature_list = []
    for i in range(0, num):
        attributes = construct_oh(home_dispatch_unit, resourcesor)
        attributes.manager_contact_info = "John Doe WAWAS Training Manager, 360-777-2316"
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


def dispatch_centers(resource_sor):

    # resource sor and home dispatch units
    dispatch_centers_ids = {'iqcs': ['AKYTDC', 'TXTIC', 'CAANCC', 'CASBCC'], 'iqs': ['AKYTDC', 'AKFASC',
                                                                                 'TXTIC', 'CABDCC', 'CALACC']}

    return dispatch_centers_ids[resource_sor]


def unit_ids(dispatch_center):
    # home dispatch unit and home unit
    d = {'AKYTDC': 'AKUYD', 'AKFASC': 'AKFAS', 'TXTIC': 'TXTXF', 'CAANCC': 'CAANF',
         'CASBCC': 'CABDF', 'CALACC': 'CALAC', 'CABDU': 'CABDUC'}

    try:
        return d[dispatch_center]
    except KeyError as e:
        return None
