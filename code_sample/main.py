import util
import page_api
'''
this is a code sample to query the IRWIN Data services rest endpoint and download data to a csv
'''

# enter credentials to generate a token
username = '*'
password = '*'

# get token
token = util.get_token(username, password)

# the url to query
endpoint_url = 'https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services' \
                   '/[OAT_NEXT]_Resources_VIEW_(Read_Only)/FeatureServer/0/query?resultOffset={}'

# specify a filter on the query
where = "1=1"

# return all results in a list of dictionaries
feature_collection = page_api.page_api(token, endpoint_url, where)

# write the feature collection to a csv file
csv_file = 'all_resources.csv'
util.response_to_dict(feature_collection, csv_file)

