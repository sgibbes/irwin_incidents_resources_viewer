import resource_util
import create_class
import test_query
import sys


# send a lastname to the resources api. Get back capability, capability type and experience.

endpoint_type = 'resource'

# the related tables
capability_url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/1/query'
capability_type_url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/3/query'
experience_url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/5/query'

# initiate class
inputs = create_class.QueryType(endpoint_type)
token = test_query.get_token(inputs.token_url, inputs.usr, inputs.pswd)

where_inputs = "NameLast = 'Abadir'"

# get the IrwinRID and use that to query capability
resource = test_query.query_api(inputs, token, where_inputs)
resource_response = test_query.load_response(resource)

if len(resource_response) > 1:
    print 'more than one response returned'
    sys.exit()
else:
    irwinrid = resource_response[0]['attributes']['IrwinRID'].strip('}').strip('{')

# set the class url to capability url
inputs.url = capability_url

# query the capability table using IrwinRID
capability_d = resource_util.query_related_tables(inputs, token, "IrwinRID = '{}'".format(irwinrid))


# query capability type table using CTID
inputs.url = capability_type_url
captype_d = resource_util.query_related_tables(inputs, token, "IrwinCTID = '{}'".format(capability_d['IrwinCTID']))


# query experience table using IrwinCID
inputs.url = experience_url
experience_d = resource_util.query_related_tables(inputs, token, "IrwinCID = '{}'".format(capability_d['IrwinCID']))

print experience_d