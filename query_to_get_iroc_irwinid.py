import create_class
import query
import add_iroc_records
import add_resource_util
import sys

# initiate class
inputs = create_class.QueryType('resource')

# generate token to query endpoint
token = query.get_token(inputs.token_url, inputs.usr, inputs.pswd)

# go through overhead resources in spreadsheet:
df = add_iroc_records.create_new_spreadsheet_from_orig('/Users/sam/Documents/IRWIN/CAD_ROW_DBUNT.csv')

for index, row in df.iterrows():

    if row['RESCAT'] == 'O':
        # get home dispatch unit
        home_dispatch_unit_id = 'CABDU'

        # construct attributes class
        attributes = add_resource_util.construct_oh(home_dispatch_unit_id, 'iroc')

        # re-assign attributes for this case
        attributes.firstname = row['NameFirst'].strip().split(" ")[0].replace("'", "")

        if len(row['NameFirst'].strip().split(" ")) > 1:
            attributes.middlename = row['NameFirst'].strip().split(" ")[1].replace("'", "")

        else:
            try:
                attributes.middlename = row['NameMiddle'].replace("'", "")
            except:
                attributes.middlename = 'A'

        attributes.lastname = row['NameLast'].replace("'", "")

        print '{} {} {}'.format(attributes.firstname, attributes.middlename, attributes.lastname)

        where_inputs = "NameFirst = '{}' AND NameLast = '{}'".format(attributes.firstname, attributes.lastname, attributes.middlename)
        response = query.query_api(inputs, token, where_inputs)

        # because of multiple uploads, just pick first one
        try:
            irwinrid = response['features'][0]['attributes']['IrwinRID']
            print irwinrid
            # row['IRWINRID'] = irwinrid
            df.at[index, 'IrwinRID'] = str(irwinrid)

        except:
            with open('errors.txt', 'a') as errorfile:
                errorfile.write(where_inputs + '\n')

df.to_csv('/Users/sam/Documents/IRWIN/CAD_ROW_DBUNT_edited_w_irwinrid_v3.csv')

# print df.head()
# # construct where clause. If user doesn't input anything, defaults to CreatedOnDateTime > 0
# where_inputs = query.where_inputs(inputs)
# print where_inputs

