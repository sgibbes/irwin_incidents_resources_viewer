import query
import sys


def get_names():
    inputs_dict = {}
    var_list = ['NameFirst', 'NameLast', 'IrwinRID']
    where = "CreatedOnDateTime > 0"

    for var in var_list:
        inputs_dict[var] = raw_input("{}: ".format(var))

    for name, val in inputs_dict.iteritems():
        if val is not '':
            # lowercase the irwin id
            # add the where clause to build where statement
            where += " AND {} = '{}'".format(name, val)

    return where


def query_related_tables(inputs, token, sql, id=None):

    # query capability table
    response = query.query_api(inputs, token, sql)

    a_list = []
    features = response['features']
    len_features = len(features)
    # print "\tnumber of Records Found: {}".format(len_features)
    if len_features > 0:

        irwin_id = None
        if id:
            irwin_id = response['features'][0]['attributes'][id]

        for d in response['features']:
            a_list.append(d)

        return a_list, irwin_id

    else:
        return None, None


def multiple_records(response, inputs, token, environment):
    for r in response:
        print '\n'
        irwinrid = r['attributes']['IrwinRID']
        print r['attributes']['NameLast']
        print r['attributes']['NameFirst']

        inputs.url = urls('capability', environment)
        sql = "IrwinRID = '{}'".format(irwinrid)
        response = query.query_api(inputs, token, sql)
        if len(response['features']) > 1:

            for k, v in response.iteritems():
                print '{}: {}'.format(k, v)
            sys.exit()


def urls(table, endpoint_type):

    url_dict = {'capability': 'https://{}.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/1/query',
    'capability_type': 'https://{}.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/3/query',
    'experience': 'https://{}.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/5/query',
    'capability_request': 'https://{}.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/2/query',
    'resource': 'https://{}.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/0/query',
    'resource_relationship': 'https://{}.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/6/query'}

    return url_dict[table].format(endpoint_type)


def format_response(resource_response, capability_d=None, captype_d=None, experience_d=None, capability_r_d=None):
    for tablename, response in {'RESOURCE': resource_response, 'CAPABILITY': capability_d, 'CAPABILITY TYPE': captype_d,
                     'EXPERIENCE': experience_d, 'CAPABILITY REQUEST': capability_r_d}.iteritems():
        if response:
            print 'TABLE: {}'.format(tablename)

            for r in response:
                if r:
                    if type(r) == list:
                        for record in r:
                            print '\n'
                            for k, v in record['attributes'].iteritems():
                                print '{}: {}'.format(k, v)
                    else:
                        for k, v in r['attributes'].iteritems():
                            print '{}: {}'.format(k, v)

                    print '\n'

            # for record in response:
            #     for k, v in record['attributes'].iteritems():
            #         print '{}: {}'.format(k, v)


def check_operational_name(resource_response):

    for dict_resp in resource_response:
        if dict_resp['attributes']['ResourceKind'] == 'Overhead':

            operational_name = dict_resp['attributes']['OperationalName']
            firstname = dict_resp['attributes']['NameFirst']
            middlename = dict_resp['attributes']['NameMiddle']
            lastname = dict_resp['attributes']['NameLast']

            # construct what operational name should be
            if middlename:
                op_name_check = '{}, {} {}'.format(lastname, firstname, middlename)
            else:
                op_name_check = '{}, {}'.format(lastname, firstname)
            if op_name_check == operational_name:
                pass
            else:
                system = dict_resp['attributes']['CreatedBySystem']
                print 'OP name error: System: {} | {} != {}'.format(system, op_name_check, operational_name)

