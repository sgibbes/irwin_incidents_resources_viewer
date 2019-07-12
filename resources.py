import resource_util
import create_class
import query
import sys

import pandas as pd
# send a lastname to the resources api. Get back capability, capability type and experience.

endpoint_type = 'resource'

# the related tables
capability_url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/1/query'
capability_type_url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/3/query'
experience_url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/5/query'

# initiate class
inputs = create_class.QueryType(endpoint_type)
token = query.get_token(inputs.token_url, inputs.usr, inputs.pswd)

# where_inputs = "1=1"
where_inputs = "NameLast = 'Collins' AND NameFirst = 'Eric'"

# get the IrwinRID and use that to query capability
resource = query.query_api(inputs, token, where_inputs)
resource_response = query.load_response(resource)

if len(resource_response) > 1:
    print 'more than one response returned'
    resource_util.multiple_records(resource_response, inputs, token)
    sys.exit()
else:
    irwinrid = resource_response[0]['attributes']['IrwinRID'].strip('}').strip('{')


# set the class url to capability url
print 'querying capability'
inputs.url = capability_url

# query the capability table using IrwinRID
capability_d, irwinctid = resource_util.query_related_tables(inputs, token, "IrwinRID = '{}'".format(irwinrid), 'IrwinCTID')

# query capability type table using CTID
print 'querying capability type'
inputs.url = capability_type_url
captype_d = resource_util.query_related_tables(inputs, token, "IrwinCTID = '{}'".format(irwinctid))[0]


# query experience table using IrwinCID
print 'querying experience '
inputs.url = experience_url

sql = "IrwinCID = '{}'".format(capability_d[0]['attributes']['IrwinCID'])

experience_d = resource_util.query_related_tables(inputs, token, sql)

for table, d in {'RESOURCE': resource_response, 'CAPABILITY': capability_d, 'CAPABILITY TYPE': captype_d,
                 'EXPERIENCE': experience_d}.iteritems():
    if d:
        print '\nTable: {}'.format(table)
        for r in d:
            print r
