import query
import sys


def get_names():
    inputs_dict = {}
    var_list = ['NameFirst', 'NameLast']
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
    # capability_response = test_query.load_response(response)

    a_list = []
    features = response['features']
    len_features = len(features)
    print "\tnumber of Records Found: {}".format(len_features)
    if len_features > 0:

        irwin_id = None
        if id:
            irwin_id = response['features'][0]['attributes'][id]

        for d in response['features']:
            a_list.append(d)

        return a_list, irwin_id

    else:
        return None, None


def multiple_records(response, inputs, token):
    for r in response:
        print '\n'
        irwinrid = r['attributes']['IrwinRID']
        print r['attributes']['NameLast']
        print r['attributes']['NameFirst']

        inputs.url = urls('capability')
        sql = "IrwinRID = '{}'".format(irwinrid)

        response = query.query_api(inputs, token, sql)
        if len(response['features']) > 1:

            print response
            sys.exit()


def urls(table):
    url_dict = {'capability': 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/1/query',
    'capability_type': 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/3/query',
    'experience': 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/5/query'}

    return url_dict[table]


def format_response(resource_response, capability_d=None, captype_d=None, experience_d=None):
    for tablename, response in {'RESOURCE': resource_response, 'CAPABILITY': capability_d, 'CAPABILITY TYPE': captype_d,
                     'EXPERIENCE': experience_d}.iteritems():
        if response:
            print '\nTable: {}'.format(tablename)
            for record in response:
                print record