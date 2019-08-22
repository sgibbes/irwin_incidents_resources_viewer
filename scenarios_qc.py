import resource_util
import create_class
import query
import sys
import pandas as pd

# Incident ID: {6E7783BC-A682-4190-8E38-D1EBDC033C43} WiresFun1
# given the IrwinID

# Query CapabilityRequest table using IrwinID

#       return the capability requests with the CID, CTID

# Query the Capability table usin ghte CID
#       return the IrwinRID

# query the Resource table using the IrwinRID
#       return the Agency and Position


#############################################################################

def given_incident_id():
    irwin_id = '{C31DB32C-8966-409F-A892-860350875C7C}'
    endpoint_type = 'resource'
    environment = 'irwinoat'
    resources = []
    resources_d = {}
    # initiate class
    inputs = create_class.QueryType(endpoint_type)
    token = query.get_token(inputs.token_url, inputs.usr, inputs.pswd)

    # Query CapabilityRequest table using IrwinID
    inputs.url = resource_util.urls('capability_request', environment)
    capreq_d = resource_util.query_related_tables(inputs, token, "IrwinID = '{}'".format(irwin_id))[0]

    for cap_req in capreq_d:

        # only use capability request records where FulfillmentStatus = Filled
        if cap_req['attributes']['FulfillmentStatus'] == 'Filled':

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

                # query resources table to get agency and operaitonal name (for readability)
                table_name = 'resource'

                inputs.url = resource_util.urls(table_name, environment)
                resource_record = resource_util.query_related_tables(inputs, token, "IrwinRID = '{}'".format(rid))[0]
                agency = resource_record[0]['attributes']['ProviderAgency']
                general_status = resource_record[0]['attributes']['GeneralStatus']
                operational_status = resource_record[0]['attributes']['OperationalStatus']

                operational_name = resource_record[0]['attributes']['OperationalName']

                # create dictionary where key is IrwinRID and values are list of: 1-Position 2-Agency
                resources_d[operational_name] = [rid, position, agency, general_status, operational_status]

    df = pd.DataFrame.from_dict(resources_d, orient="index")

    df = df.reset_index()

    df = df.rename(columns={'index': 'OperationalName', 0: 'IrwinRID', 1: 'Position', 2: 'ProviderAgency'})

    print df
    grouped = df.groupby(['Position', 'ProviderAgency']).count()

    df2 = df[['Position', 'ProviderAgency']]

    pivoted = df2.pivot_table(index='Position', columns='ProviderAgency', aggfunc=len)

    print pivoted


def get_roster_info():
    endpoint_type = 'resource'
    environment = 'irwinoat'
    inputs = create_class.QueryType(endpoint_type)
    token = query.get_token(inputs.token_url, inputs.usr, inputs.pswd)

    overhead_resources_opname = ['E3553Test']

    for oh in overhead_resources_opname:
        print 'Results for: {}'.format(oh)
        table_name = 'resource'

        inputs.url = resource_util.urls(table_name, environment)
        response = resource_util.query_related_tables(inputs, token, "ApparatusNumber = '{}'".format(oh))[0]
        rid = response[0]['attributes']['IrwinRID']
        print '\tIrwinRID: {}'.format(rid)

        # get irwin cid:
        table_name = 'capability'

        inputs.url = resource_util.urls(table_name, environment)
        response = resource_util.query_related_tables(inputs, token, "IrwinRID = '{}'".format(rid))[0]
        cid = response[0]['attributes']['IrwinCID']
        ctid = response[0]['attributes']['IrwinCTID']
        print '\tIrwinCID: {}'.format(cid)
        print '\tIrwinCTID: {}'.format(ctid)

        # look up the capability request
        table_name = 'capability_request'

        inputs.url = resource_util.urls(table_name, environment)
        response = resource_util.query_related_tables(inputs, token, "IrwinCID = '{}'".format(cid))[0]

        print response
        # for r in response:
        #     print r['attributes']['IrwinCID']
        #     print r['attributes']['IrwinCTID']
        # sys.exit()
        # query resource relationship table using childIrwinCID
        table_name = 'resource_relationship'

        inputs.url = resource_util.urls(table_name, environment)
        response = resource_util.query_related_tables(inputs, token, "ChildIrwinCID = '{}'".format(cid))[0]
        parent_rid = response[0]['attributes']['ParentIrwinRID']
        print '\tParentIrwinRID: {}'.format(parent_rid)

        # query reousrce table to get parent Operaitonal Name
        table_name = 'resource'

        inputs.url = resource_util.urls(table_name, environment)
        response = resource_util.query_related_tables(inputs, token, "IrwinRID = '{}'".format(parent_rid))[0]
        parent_operational_name = response[0]['attributes']['OperationalName']

        print '\tParent Operational Name: {}'.format(parent_operational_name)

get_roster_info()


# 3 resources that are on an engine and their capability types
# 'Barriga, Manuel F',