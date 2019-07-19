import add_resource_util
import create_class
import query

import pandas as pd

import sys
# add list of records from excel sheet to irwin test environment. add overhead resources. add capabilities
# into capability type table


def get_existing_oh_resource(token, sql):
    url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/0/Query'

    endpoint_type = 'resource'

    # initiate class
    inputs = create_class.QueryType(endpoint_type)
    inputs.url = url
    resource = query.query_api(inputs, token, sql)

    if len(resource['features']) > 0:
        return True

    else:
        return False

def get_capability_type_id(token, sql):
    url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/3/Query'

    endpoint_type = 'resource'

    # initiate class
    inputs = create_class.QueryType(endpoint_type)
    inputs.url = url
    resource = query.query_api(inputs, token, sql)

    if len(resource['features']) > 0:
        return str(resource['features'][0]['attributes']['IrwinCTID'])

    else:
        print 'POSITION CODE NOT FOUND'


def add_record(json_feature, url, token):

    json_feature_list = [json_feature]

    # send json feature to the add-query
    response = add_resource_util.query_api(url, token, json_feature_list)

    # check if they were successfully added
    if not response['addResults'][0]['success']:
        print 'ERROR: \m'
        print response['addResults'][0]['error']

    else:
        print 'SUCCESS!'

    return response


def create_new_spreadsheet():
    df = pd.read_csv('/Users/sam/Documents/IRWIN/CAD_ROW_DBUNT_edited copy.csv')

    # just select overhead resource
    df = df[df.ResourceKind == "O"]

    # get first, last name
    df['NameLast'], df['NameFirst'] = df['name'].str.split(',', 1).str

    # make up middle
    df['NameMiddle'] = 'A'

    return df


def add_iroc_oh_resources():
    # set up url, token, etc
    token_url = 'https://irwinoat.doi.gov/arcgis/tokens/generateToken?'
    token = query.get_token(token_url, 'qualification_test', 'Testing!Testing!123')

    df = create_new_spreadsheet()

    for index, row in df.iterrows():

        # get home dispatch unit
        home_dispatch_unit_id = row['HomeUnit_HomeDispatchUnit_CurrentDispatchUnit']

        # construct attributes class
        attributes = add_resource_util.construct_oh(home_dispatch_unit_id, 'iroc')

        # re-assign attributes for this case
        attributes.firstname = row['NameFirst'].strip().split(" ")[0].replace("'", "")

        if len(row['NameFirst'].strip().split(" ")) > 1:
            attributes.middlename = row['NameFirst'].strip().split(" ")[1].replace("'", "")

        else:
            attributes.middlename = row['NameMiddle'].replace("'", "")

        attributes.lastname = row['NameLast'].replace("'", "")

        attributes.jet_port = 'SMF'
        attributes.home_unit = home_dispatch_unit_id
        attributes.resource_clearinghouse_id = row['ResourceClearinghouseID']
        attributes.manager_contact_info = 'Robert Matsueda'
        attributes.primary_email = ''
        or_json_feature = add_resource_util.feature(attributes)

        # query to make sure firename, lastname doesn't already exist, if so, pass
        sql = "NameFirst = '{}' AND NameLast = '{}'".format(attributes.firstname, attributes.lastname)
        print sql

        if get_existing_oh_resource(token, sql):
            print 'resources already exists, skip'
            pass

        else:
            print 'keep going'

            print '\n\nADDING OVERHEAD RESOURCE: {} {}\n\n'.format(attributes.firstname, attributes.lastname)

            # url to add fetures to irwin test
            url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/0/addFeatures'
            response = add_record(or_json_feature, url, token)

            if not response['addResults'][0]['success']:
                print 'not a success'
                pass

            else:
                # get the irwin RID back
                irwinrid = str(response['addResults'][0]['irwinRID'])

                # create a related record in the capability table
                position_code = row['Position']
                sql = "Kind = 'Overhead' AND Category = 'Position' AND PositionCode = '{}'".format(position_code)

                # query the capability type table to get capability type id
                irwin_ctid = get_capability_type_id(token, sql)

                print '\nIrwinCTID: {}'.format(irwin_ctid)
                print '\nIrwinRID: {}'.format(irwinrid)
                print '\nPosition code: {}'.format(position_code)

                # add record in the capability table
                capability_type_json_feature = add_resource_util.capability_type(irwin_ctid, irwinrid)

                url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/1/addFeatures'

                print 'ADDING RELATED RECORD IN CAPABILITY TABLE'
                response = add_record(capability_type_json_feature, url, token)


def find_missing_position_codes():
    token_url = 'https://irwinoat.doi.gov/arcgis/tokens/generateToken?'
    token = query.get_token(token_url, 'qualification_test', 'Testing!Testing!123')

    df = create_new_spreadsheet()

    position_codes = []
    for index, row in df.iterrows():
        position_code = row['Position']
        position_codes.append(position_code)


    position_codes_unique = set(position_codes)

    for code in position_codes_unique:
        sql = "Kind = 'Overhead' AND Category = 'Position' AND PositionCode = '{}'".format(code)
        print 'POSITION CODE: {}'.format(code)
        irwin_ctid = get_capability_type_id(token, sql)


add_iroc_oh_resources()