
import query
import sys


def query_related_tables(inputs, token, sql, id=None):

    # query capability table

    response = query.query_api(inputs, token, sql)
    # capability_response = test_query.load_response(response)

    a_list = []
    features = response['features']
    len_features = len(features)
    print "Number of Records Found: {}".format(len_features)
    if len_features > 0:

        irwin_id = None
        if id:
            irwin_id = response['features'][0]['attributes'][id]

        for d in response['features']:
            a_list.append(d)

        return a_list, irwin_id

    else:
        return None

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

