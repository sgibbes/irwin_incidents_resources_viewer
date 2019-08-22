import resource_util
import create_class
import query
import sys
 # rid for testing: {A88C7349-A857-42F6-B5AB-353D7E238C70}
 # should have 2 capability requests: {A88C7349-A857-42F6-B5AB-353D7E238C70}
 # capabilityid {92CAD3A0-61CC-4159-9E39-C07642C195AF}
# send a lastname to the resources api. Get back capability, capability type and experience.
# first capability request id: {C621A7CA-8E45-4B84-A3C9-CDDADA5DF9D2}
# second capability request id : D82BDC02-2EE1-4AAE-872F-7CF8C2D705A4
endpoint_type = 'resource'
environment = 'irwinoat'
# initiate class
inputs = create_class.QueryType(endpoint_type)
token = query.get_token(inputs.token_url, inputs.usr, inputs.pswd)

# where_inputs = "1=1"
# where_inputs = "NameLast = 'Collins' AND NameFirst = 'Eric'"
where_inputs = resource_util.get_names()

# get the IrwinRID and use that to query capability
resource = query.query_api(inputs, token, where_inputs)

resource_response = query.load_response(resource)

if len(resource_response) == 0:
    print 'No Records Found'
    sys.exit()

if len(resource_response) > 1:
    print 'more than one response returned'
    resource_util.multiple_records(resource_response, inputs, token, environment)
    sys.exit()

else:
    irwinrid = resource_response[0]['attributes']['IrwinRID'].strip('}').strip('{')
    print 'IrwinRID: {}'.format(irwinrid)

# set the class url to capability url
print '\nQuerying capability:'
inputs.url = resource_util.urls('capability', environment)

sql = "IrwinRID = '{}'".format(irwinrid)

# query the capability table using IrwinRID
capability_d, irwinctid = resource_util.query_related_tables(inputs, token, sql, 'IrwinCTID')

if not irwinctid:
    resource_util.format_response(resource_response, capability_d)
    sys.exit()

# query capability type table using CTID
print '\nQuerying capability type'
inputs.url = resource_util.urls('capability_type', environment)
captype_d = resource_util.query_related_tables(inputs, token, "IrwinCTID = '{}'".format(irwinctid))[0]

# query experience table using IrwinCID
print '\nQuerying experience '
inputs.url = resource_util.urls('experience', environment)

irwin_cid = capability_d[0]['attributes']['IrwinCID']

sql = "IrwinCID = '{}'".format(irwin_cid)

experience_d = resource_util.query_related_tables(inputs, token, sql)
#############################################
# print '\nQuerying Capability Request '
# # query capability request: need
# # IrwinID- the id of the incident,
# # IrwinCTID, the capability type ID returned from querying cpability type table
# # IrwinCID:
# sql = "IrwinID = '4A34CB7A-62AE-478D-931F-8FE4090FEDED' AND " \
#       "IrwinCTID = '{}' AND " \
#       "IrwinCID = '{}'".format(irwinctid, irwin_cid)
# inputs.url = resource_util.urls('capability_request', environment)
#
# capability_r_d = resource_util.query_related_tables(inputs, token, sql)[0]

#############################################
if experience_d[0]:
    print '\nQuerying Incident'


#############################################
print "\nRESULTS:\n"
resource_util.format_response(resource_response, capability_d, captype_d, experience_d)

