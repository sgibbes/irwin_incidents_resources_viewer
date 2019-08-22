import pandas as pd
import sys

import query
import add_resource_util
from add_iroc_records import get_existing_oh_resource, add_record

# open a spreadsheet which has fields we want

# construct json text to add records

# add records

# return the irwin rid and put back into the spreadsheet


env = 'irwinoat'
query_resource_url = 'https://{}.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/0/Query'.format(env)

token_url = 'https://{}.doi.gov/arcgis/tokens/generateToken?'.format(env)

add_resource_url = 'https://{}.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/0/addFeatures'.format(env)

token = query.get_token(token_url, 'ordering_test', 'Testing!Testing!123')

df = pd.read_csv('/Users/sam/Documents/IRWIN/EquipmentToAdd_CABDCC.csv')

for index, row in df.iterrows():
    a = add_resource_util.construct_oh('CABDCC', 'iroc')

    a.resource_kind = "Equipment"
    a.app_num = row['Apparatus Number']
    a.home_unit = 'CABDU'
    a.provider_unit = 'CABDU'
    a.serial_num = row['Serial Number']
    a.vin = row['VIN']

    equip_json_feature = add_resource_util.equipment_add(a)

    # check if it exists
    sql = "VIN = '{}'".format(a.vin)
    print sql

    if get_existing_oh_resource(token, sql, query_resource_url):
        print 'already exists'
        with open('errors.txt', 'a') as errorfile:
            errorfile.write('Already exists: {}\n'.format(sql))
        pass

    else:

        response = add_record(equip_json_feature, add_resource_url, token)
        if not response['addResults'][0]['success']:
            print 'not a success'
            with open('errors.txt', 'a') as errorfile:
                errorfile.write('not a success: {}\n'.format(sql))

            pass

        else:
            # get the irwin RID back
            irwinrid = str(response['addResults'][0]['irwinRID'])

            # add irwin rid to spreadsheet:
            df.at[index, 'IrwinRID'] = irwinrid

df.to_csv('/Users/sam/Documents/IRWIN/equipment_w_irwinrid.csv')
