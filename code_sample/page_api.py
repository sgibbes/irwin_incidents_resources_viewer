import pandas as pd

from util import *


def page_api(token):
    '''
    Here are a few where clauses to try. Always leave the OBJECTID > {} in

    To gather all records for any of the tables:
    where = "OBJECTID > {}"

    Some tables have thousands of records so to test, try a specific query. This one is for Resources (table 0)
    where = "OBJECTID > {} AND ResourceKind = 'Overhead' AND OperationalStatus = 'At Incident'"

    # to query the capability table (table # 2), first test using a specific where clause:
    where = "OBJECTID > {} AND IrwinRID = '903E8D5D-7337-43BC-92CF-B1CDA5AB2468'"

    '''
    # this will iterate over records, using the objectid to identify where previous batch stopped
    counter = 0

    # some tables have thousands of records so to test, try a specific query:
    where = "OBJECTID > {} AND ResourceKind = 'Overhead' AND OperationalStatus = 'At Incident'"

    # create empty list to store each record
    feature_coll = {'features': []}

    # set response to true, when no more records are returned, set this to false
    response = True

    # the endpoint url to query. Change the 0 to 1,2,...7 to get the different tables
    endpoint_url = 'https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services' \
                   '/[OAT_NEXT]_Resources_VIEW_(Read_Only)/FeatureServer/0/query'

    # get the first 2,000 records, setting where to OBJECTID > 0
    first_batch = query_api(endpoint_url, token, where.format(0))

    if 'error' in first_batch.keys():
        print first_batch['error']

    # add results to the list of features
    feature_coll['features'].extend(first_batch['features'])

    # get min and max obj id for next query, but really only need max objectid
    min_obj, max_obj = min_max_objid(first_batch)

    # get the number of records returned, so that when it is 0, can exit loop
    len_of_response = len(first_batch['features'])

    # while our response is true
    while response:

        # set value of last reponse length to the current response length, this will get updated later
        len_of_last_response = len_of_response

        # increase counter, useful to know how many iterations have been done
        counter += 1
        print 'iteration number: {}'.format(counter)

        # query api using where clause, set Objectid > max objectid of last batch
        next_batch = query_api(endpoint_url, token, where.format(max_obj))

        print 'min/max of batch above: {}, {}'.format(min_obj, max_obj)

        # catch any errors returned by API
        if 'error' in next_batch.keys():
            print next_batch['error']
        print len(next_batch['features'])

        # the # of records returned should always be equal to max records allowed by API
        # unless on last iteration. otherwise, something is wrong
        len_of_response = len(next_batch['features'])

        if len_of_response > len_of_last_response:
            print 'length of this response is less than length of last response, exiting'
            sys.exit()

        # exit loop if next query returns 0 features
        if len(next_batch['features']) == 0:
            print 'batch is 0. settings response to false.'

            response = False

        # keep querying using max id of previous batch
        else:
            print 'length greater than 0. appending to feature collection'

            feature_coll['features'].extend(next_batch['features'])

            min_obj, max_obj = min_max_objid(next_batch)

    # put attributes into dictionary
    attributes = []
    for f in feature_coll['features']:

        try:
            # add geometry to the attributes as a new key
            f['attributes']['geometry'] = f['geometry']

        except:
            pass

        attributes.append(f['attributes'])

    df = pd.DataFrame(attributes)
    df.to_csv('irwin_oatnext.csv')