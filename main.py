import create_class
import test_query
import sys


'''
irwin data - the read only IRWIN Incident Data endpoint - 782F7530-EAF2-4803-91EC-96AA3067DB94
api - the read-only production endpoint used by irwinreadonly - 782F7530-EAF2-4803-91EC-96AA3067DB94
oat - 06840910-91C2-4CD5-A155-00C626005335
test- 31F05494-AB62-4D2B-93AE-020147903814
oat next - 37E68F0B-2A06-4216-9FE2-00060749B4E1
resource = https://irwinoat.doi.gov/observer/resources/?v=next - RID = 2018920D-3C07-40E0-87E1-009DB18A9159 -object id: 53603

'''
# get endpoint type which is only info needed
endpoint_type = raw_input("ENDPOINT TYPE: ")

# initiate class
inputs = create_class.QueryType(endpoint_type)

# generate token to query endpoint
token = test_query.get_token(inputs.token_url, inputs.usr, inputs.pswd)

# construct where clause. If user doesn't input anything, defaults to CreatedOnDateTime > 0
where_inputs = test_query.where_inputs(inputs)
print where_inputs
sys.exit()
'''
irwin data/ api id
312c4f1f-e148-4531-b7dd-49fc5e2136d8


'''
# query the desired endpoint

response = test_query.query_api(inputs, token, where_inputs)

# return data
test_query.load_response(response)

