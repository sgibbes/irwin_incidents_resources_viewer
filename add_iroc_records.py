import add_resource_util
import create_class
import query

import pandas as pd

import sys
# add list of records from excel sheet to irwin test environment. add overhead resources. add capabilities
# into capability type table


def get_capability_type_id(token, sql):
    url = 'https://irwint.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/3/Query'

    endpoint_type = 'resource'

    # initiate class
    inputs = create_class.QueryType(endpoint_type)
    inputs.url = url
    resource = query.query_api(inputs, token, sql)

    return str(resource['features'][0]['attributes']['IrwinCTID'])


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
    df = pd.read_csv('/Users/sam/Documents/IRWIN/CAD_ROW_DBUNT_edited.csv')

    # just select overhead resource
    df = df[df.ResourceKind == "O"]

    # get first, last name
    df['NameLast'], df['NameFirst'] = df['name'].str.split(',', 1).str

    # make up middle
    df['NameMiddle'] = 'A'

    return df

# set up url, token, etc
token_url = 'https://irwint.doi.gov/arcgis/tokens/generateToken?'
token = query.get_token(token_url, 'qualification_test', 'Testing!Testing!123')




df = create_new_spreadsheet()

for index, row in df.head(n=2).iterrows():

    # get home dispatch unit
    home_dispatch_unit_id = row['HomeUnit_HomeDispatchUnit_CurrentDispatchUnit']

    # construct attributes class
    attributes = add_resource_util.construct_oh(home_dispatch_unit_id, 'iroc')

    # re-assign attributes for this case
    attributes.firstname = row['NameFirst'].strip().split(" ")[0]

    if len(row['NameFirst'].strip().split(" ")) > 1:
        attributes.middlename = row['NameFirst'].strip().split(" ")[1]

    else:
        attributes.middlename = row['NameMiddle']

    attributes.lastname = row['NameLast']

    attributes.jet_port = 'SMF'
    attributes.home_unit = home_dispatch_unit_id
    attributes.resource_clearinghouse_id = row['ResourceClearinghouseID']
    attributes.manager_contact_info = 'Robert Matsueda'
    attributes.primary_email = ''
    or_json_feature = add_resource_util.feature(attributes)

    print '\n\nADDING OVERHEAD RESOURCE: {} {}\n\n'.format(attributes.firstname, attributes.lastname)
    # url to add fetures to irwin test
    url = 'https://irwint.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/0/addFeatures'
    response = add_record(or_json_feature, url, token)

    if not response['addResults'][0]['success']:
        print 'not a success'
        pass

    else:
        # get the irwin RID back
        # irwinrid = '{9F8C168A-D8F2-453B-B0AE-69BC6FCA7850}'
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

        url = 'https://irwint.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/1/addFeatures'

        print 'ADDING RELATED RECORD IN CAPABILITY TABLE'
        response = add_record(capability_type_json_feature, url, token)






