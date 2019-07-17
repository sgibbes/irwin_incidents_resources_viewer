import resource_util
import create_class
import query
import sys

# send a lastname to the resources api. Get back capability, capability type and experience.

endpoint_type = 'resource'

# initiate class
inputs = create_class.QueryType(endpoint_type)
token = query.get_token(inputs.token_url, inputs.usr, inputs.pswd)

where_inputs = "1=1"
# where_inputs = "NameLast = 'Collins' AND NameFirst = 'Eric'"
# where_inputs = resource_util.get_names()

# get the IrwinRID and use that to query capability
resource = query.query_api(inputs, token, where_inputs)

resource_response = query.load_response(resource)

if len(resource_response) == 0:
    print 'No Records Found'
    sys.exit()

if len(resource_response) > 1:
    print 'more than one response returned'
    resource_util.multiple_records(resource_response, inputs, token)
    sys.exit()
else:
    irwinrid = resource_response[0]['attributes']['IrwinRID'].strip('}').strip('{')
    print 'IrwinRID: {}'.format(irwinrid)

# set the class url to capability url
print '\nQuerying capability:'
inputs.url = resource_util.urls('capability')
sql = "IrwinRID = '{}'".format(irwinrid)

# query the capability table using IrwinRID
capability_d, irwinctid = resource_util.query_related_tables(inputs, token, sql, 'IrwinCTID')

if not irwinctid:
    resource_util.format_response(resource_response, capability_d)
    sys.exit()

# query capability type table using CTID
print '\nQuerying capability type'
inputs.url = resource_util.urls('capability_type')
captype_d = resource_util.query_related_tables(inputs, token, "IrwinCTID = '{}'".format(irwinctid))[0]


# query experience table using IrwinCID
print '\nQuerying experience '
inputs.url = resource_util.urls('experience')

sql = "IrwinCID = '{}'".format(capability_d[0]['attributes']['IrwinCID'])

experience_d = resource_util.query_related_tables(inputs, token, sql)


print "\nRESULTS:\n"
resource_util.format_response(resource_response, capability_d, captype_d, experience_d)

