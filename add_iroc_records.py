import add_resource_util
import create_class
import query

import pandas as pd

import sys
# add list of records from excel sheet to irwin test environment. add overhead resources. add capabilities
# into capability type table


def get_existing_oh_resource(token, sql, url):
    print token
    print sql
    print url
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


def create_new_spreadsheet_from_orig(in_sheet=None):

    if in_sheet:
        df = pd.read_csv(in_sheet)
    else:
        df = pd.read_csv('/Users/sam/Documents/IRWIN/CAD_ROW_DBUNT_edited.csv')
    # get first, last name
    df['NameLast'], df['NameFirst'] = df['ROSNAME'].str.split(',', 1).str

    return df


def create_new_spreadsheet(in_sheet=None):

    if in_sheet:
        df = pd.read_csv(in_sheet)
    else:
        df = pd.read_csv('/Users/sam/Documents/IRWIN/CAD_ROW_DBUNT_edited.csv')
        # df = pd.read_csv('/Users/sam/Documents/IRWIN/CAD_ROW_DBUNT_edited_test.csv')
    # just select overhead resource
    df = df[df.ResourceKind == "O"]

    # get first, last name
    df['NameLast'], df['NameFirst'] = df['name'].str.split(',', 1).str
    df['NameMiddle'] = ''
    return df


def add_iroc_oh_resources():
    query_resource_url = 'https://irwint.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/0/Query'
    # query_resource_url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/0/Query'

    capability_type_url = 'https://irwint.doi.gov/arcgis/rest/services/Resource/FeatureServer/1/addFeatures'
    # capability_type_url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/1/addFeatures'

    token_url = 'https://irwint.doi.gov/arcgis/tokens/generateToken?'
    # token_url = 'https://irwinoat.doi.gov/arcgis/tokens/generateToken?'

    add_overhead_url = 'https://irwint.doi.gov/arcgis/rest/services/Resource/FeatureServer/0/addFeatures'
    # add_overhead_url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/0/addFeatures'

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
        if get_existing_oh_resource(token, sql, query_resource_url):
            print "already exists, pass\n"
            with open('errors.txt', 'a') as errorfile:
                errorfile.write('Already exists: {}\n'.format(sql))
            pass

        else:
            print '\n\nADDING OVERHEAD RESOURCE: {} {}'.format(attributes.firstname, attributes.lastname)

            response = add_record(or_json_feature, add_overhead_url, token)

            if not response['addResults'][0]['success']:
                print 'not a success'
                with open('errors.txt', 'a') as errorfile:
                    errorfile.write('not a success: {}\n'.format(sql))

                pass

            else:
                # get the irwin RID back
                irwinrid = str(response['addResults'][0]['irwinRID'])

                # add irwin rid to spreadsheet:
                df.at[index, 'IrwinRID'] = str(irwinrid)

                # create a related record in the capability table
                position_code = row['Position']
                sql = "Kind = 'Overhead' AND Category = 'Position' AND PositionCode = '{}'".format(position_code)

                # query the capability type table to get capability type id
                irwin_ctid = get_capability_type_id(token, sql)

                # add record in the capability table
                capability_type_json_feature = add_resource_util.capability_type(irwin_ctid, irwinrid)

                print 'ADDING RELATED RECORD IN CAPABILITY TABLE'
                add_record(capability_type_json_feature, capability_type_url, token)

    df.to_csv('/Users/sam/Documents/IRWIN/CAD_ROW_DBUNT_edited_w_irwinrid_v2.csv')


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
