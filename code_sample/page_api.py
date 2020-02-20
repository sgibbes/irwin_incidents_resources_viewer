from util import *


def page_api(token, endpoint_url, where):

    # use the REST api's resultOffset parameter to increment returned results by 2,000
    result_offset = 0

    # create empty list to store each record json
    feature_coll = {'features': []}

    # set this to True to start the while loop
    limit_exceeded = True

    while limit_exceeded:

        print 'result offset: {}'.format(result_offset)

        # query api using result offset
        next_batch = query_api(endpoint_url.format(result_offset), token, where)

        print len(next_batch['features'])

        # catch any errors returned by API
        if 'error' in next_batch.keys():
            print next_batch['error']

        # append results to feature collection
        feature_coll['features'].extend(next_batch['features'])

        # increment result offset to get the next 2,000 records
        result_offset += 2000

        # set the value for limit_exceeded
        if 'exceededTransferLimit' in next_batch.keys():
            limit_exceeded = next_batch['exceededTransferLimit']

        else:
            limit_exceeded = False

        print 'Transfer limit exceeded: {}'.format(limit_exceeded)

    return feature_coll

