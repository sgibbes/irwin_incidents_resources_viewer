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


def equipment_add(a):

    json_features = {
            "attributes": {
              "ApparatusNumber": a.app_num,
              "GeneralStatus": "Available",
              "HomeDispatchUnit": a.homedispatchunit,
              "HomeUnit": a.home_unit,
              "IsLocationTrackingEnabled": 1,
              "IsNationalResource": 0,
              "ResourceKind": "Equipment",
              "ManagerContactInfo": "person@mail.com",
              "ProviderUnit": a.provider_unit,
              "SerialNumber": a.serial_num,
              "ResourceSOR": a.resourcesor,
              "VIN": a.vin,
            },
            "geometry": {
              "x": -97.947200,
              "y": 32.185950
            }
        }

    return json_features



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
                "x": -117.98583499999995,
                "y": 34.25935500000003
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

        # initiate class
        attributes = construct_oh(home_dispatch_unit, resourcesor)

        # customize some attributes
        attributes.manager_contact_info = "John Doe WAWAS Training Manager, 360-777-2316"

        # send the attributes class to the json template and fill it in

        json_feature = feature(attributes)
        print '\n\n'
        for k, v in json_feature.iteritems():
            print '{}: {}'.format(k, v)
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
    dispatch_centers_ids = {'iqcs': ['AKYTDC', 'TXTIC', 'CAANCC', 'CASBCC'],
                            'iqs': ['AKYTDC', 'AKFASC', 'TXTIC', 'CABDCC', 'CALACC']}

    return dispatch_centers_ids[resource_sor]


def unit_ids(dispatch_center):

    # home dispatch unit and home unit
    d = {'AKYTDC': 'AKUYD',
         'AKFASC': 'AKFAS',
         'TXTIC': 'TXTXF',
         'CAANCC': 'CAANF',
         'CASBCC': 'CABDF',
         'CALACC': 'CALAC',
         'CABDCC': 'CABDU'}

    try:
        return d[dispatch_center]
    except KeyError as e:
        return None


def dispatch_center_coords(dispatch_center):
    d = {'AKYTDC': {'x': -147.6254, 'y': 64.8022},
         'AKUYD': {'x': -144.2206, 'y': 67.8946},
         'AKFASC': {'x': -148.3543, 'y': 64.8774},
         'TXTIC': {'x': -94.6657, 'y': 31.3382},
         'CAANCC': {'x': -118.2527, 'y': 34.7191},
         'CASBCC': {'x': -117.2089, 'y': 34.1286},
         'CALACC': {'x': -118.7548, 'y': 34.1130},
         'CABDCC': {'x': -117.2900, 'y': 34.1100}}

    return d[dispatch_center]
