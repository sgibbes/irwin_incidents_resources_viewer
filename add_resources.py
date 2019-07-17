import query
import add_resource_util
import sys
# generate different resources and send to irwin test environment as new features
'''
IQCS - 40 overhead resources in each dispatch center 
AKYTDC, AFFASC, TXTIC, CANCC, CASBCC, CALAC

IQS - 40 overhead resources in each dispatch center
AKYTDC, AFFASC, TXTIC, CANCC, CASBCC, CALAC

IROC - 40 overhead resources in each dispatch center 
AKYTDC, AFFASC, TXTIC, CANCC, CASBCC, CALAC, CABDCC


IROC - 3 aircraft resources in each dispatch center
AAKYTDC, AFFASC, TXTIC, CANCC, CASBCC, CALAC, CABDCC

1 should be Type 1 airtanker (IsNationalResource = True)
1 should be helicopter
1 should be a SEAT

IROC - 5 equipment resources in each dispatch center
AKYTDC, AFFASC, TXTIC, CANCC, CASBCC, CALAC, CABDCC

IROC - 2 crew resources in dispatch center 
1 crew with IsNationalResource = True (Type 1)
1 crew as Type 2 IA
AKYTDC, AFFASC, TXTIC, CANCC, CASBCC, CALAC, CABDCC
'''
# Log in as qualification_test
token_url = 'https://irwint.doi.gov/arcgis/tokens/generateToken?'
token = query.get_token(token_url, 'qualification_test', 'Testing!Testing!123')

# url to add fetures to irwin test
url = 'https://irwint.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/0/addFeatures'


def add_oh_resources(resource_sor):

    dispatch_center = ['AKYTDC', 'AKFASC', 'TXTIC', 'CANCC', 'CASBCC', 'CALAC']

    for d in dispatch_center:

        # generate n number of resources
        print 'home dispatch unit: {}'.format(d)
        json_features = add_resource_util.create_many_resources(1, d, resource_sor)

        # send resources to addFeatures endpoint
        response = add_resource_util.query_api(url, token, json_features)

        # check if they were successfully added
        if not response['addResults'][0]['success']:
            print 'ERROR: \m'
            print response['addResults'][0]['error']

        else:
            print 'SUCCESS!'


add_oh_resources('iqcs')
add_oh_resources('iqs')
