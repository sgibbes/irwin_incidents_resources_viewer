import util
import page_api
'''
this is a code sample to query the IRWIN Data services rest endpoint and download data to a csv
'''

# enter credentials to generate a token
username = '*'
password = '*'

token = util.get_token(username, password)

page_api.page_api(token)

