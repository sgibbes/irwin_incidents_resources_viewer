import create_class
import query
import sys

inputs = create_class.QueryType('resource')
inputs.url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/3/query'
token = query.get_token(inputs.token_url, inputs.usr, inputs.pswd)

var_list = ['Kind', 'Category', 'Type']
where = query.where_inputs(inputs, var_list)

# print where
# where = "Category = 'Strike Team' AND Type = 'Type 1' AND Kind = 'Crews'"
response = query.query_api(inputs, token, where)

# return data
print query.load_response(response)
