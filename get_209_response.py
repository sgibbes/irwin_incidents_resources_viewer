import resource_util
import create_class
import query
import sys
import pandas as pd
from tabulate import tabulate

# Incident ID: {6E7783BC-A682-4190-8E38-D1EBDC033C43} WiresFun1
# given the IrwinID

# Query CapabilityRequest table using IrwinID

#       return the capability requests with the CID, CTID

# Query the Capability table usin ghte CID
#       return the IrwinRID

# query the Resource table using the IrwinRID
#       return the Agency and Position

# Wires 209 {A6C24D05-7985-48A6-BB5D-1433B8C1DFB9}

#############################################################################
irwin_id = raw_input("IrwinID (in brackets, no quotes): ")

# irwin_id = '{5394A5C4-BCB6-4C51-A166-F7085D62D108}'
endpoint_type = 'resource'
environment = 'irwinoat'
resources = []
resources_d = {}
# initiate class
inputs = create_class.QueryType(endpoint_type)
token = query.get_token(inputs.token_url, inputs.usr, inputs.pswd)

# Query CapabilityRequest table using IrwinID
table_name = 'capability_request'
inputs.url = resource_util.urls(table_name, environment)
capreq_d = resource_util.query_related_tables(inputs, token, "IrwinID = '{}'".format(irwin_id))[0]
print '\n{0}GENERATING 209 REPORT FOR INCIDENT: {1}{0}'.format('*'*4, irwin_id)

print '\nNUMBER OF CAPABILITY REQUESTS FOUND: {}'.format(len(capreq_d))

for cap_req in capreq_d:
    print '\t\n\nCAPABILITY REQUEST FOR INCIDENT: {}'.format(irwin_id)

    fulfillment_status = cap_req['attributes']['FulfillmentStatus']

    print '\tFulfillment Status: {}'.format(fulfillment_status)

    # only use capability request records where FulfillmentStatus = Filled
    if fulfillment_status == 'Filled':

        # get the IrwinCID, IrwinCTID
        cid = cap_req['attributes']['IrwinCID']
        ctid = cap_req['attributes']['IrwinCTID']

        # query capability table to get IrwinRID
        table_name = 'capability'

        inputs.url = resource_util.urls(table_name, environment)
        cap_d = resource_util.query_related_tables(inputs, token, "IrwinCID = '{}'".format(cid))[0]

        # iterate over each capability record
        for cap in cap_d:

            # get the resource associated with that Capability ID
            rid = cap['attributes']['IrwinRID']

            # query capability type table to get Position
            table_name = 'capability_type'

            inputs.url = resource_util.urls(table_name, environment)
            cap_type = resource_util.query_related_tables(inputs, token, "IrwinCTID = '{}'".format(ctid))[0]
            position = cap_type[0]['attributes']['PositionCode']

            if not position:
                position = cap_type[0]['attributes']['Category']
            # query resources table to get agency and operaitonal name (for readability)
            table_name = 'resource'

            inputs.url = resource_util.urls(table_name, environment)
            resource_record = resource_util.query_related_tables(inputs, token, "IrwinRID = '{}'".format(rid))[0]

            operational_status = resource_record[0]['attributes']['OperationalStatus']

            # only count resources that are at the incident

            if operational_status == 'At Incident':
                agency = resource_record[0]['attributes']['ProviderAgency']
                general_status = resource_record[0]['attributes']['GeneralStatus']

                operational_name = resource_record[0]['attributes']['OperationalName']

                # create dictionary where key is IrwinRID and values are list of: 1-Position 2-Agency
                resources_d[operational_name] = [rid, position, agency, general_status, operational_status]
    else:

        print 'No Capability Request Records Found'


print '\n\n\n'
df = pd.DataFrame.from_dict(resources_d, orient="index")

df = df.reset_index()

df = df.rename(columns={'index': 'OperationalName', 0: 'IrwinRID', 1: 'Position',
                        2: 'ProviderAgency', 3: 'GeneralStatus', 4: 'OperationalStatus'})

# print df
print(tabulate(df, headers='keys', tablefmt='psql'))
grouped = df.groupby(['Position', 'ProviderAgency']).count()

df2 = df[['Position', 'ProviderAgency']]

pivoted = df2.pivot_table(index='Position', columns='ProviderAgency', aggfunc=len)

# print pivoted

print(tabulate(pivoted, headers='keys', tablefmt='psql'))





