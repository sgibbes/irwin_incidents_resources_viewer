'''

for reference:
input is:
- irwin data
- irwin test
- irwin oat

'''
import json
import sys
import os


class QueryType:

    def __init__(self, url_type, environment):

        self.url_type = url_type

        self.environment = environment
        self.input_user_type = None

        self.usr = None
        self.pswd = None
        self.url = None

        self.token_url = None

        self.id = None

        self.out_fields = None

        # get irwin id name
        self.get_id()

        # set which url to query
        self.get_url()

        # set up username/password
        self.get_creds()

        # set the fields to return with the response
        self.set_outfields()

    def set_outfields(self):
        if self.url_type == 'resource':
            self.out_fields = 'IrwinRID'
        else:
            self.out_fields = 'FireDiscoveryDateTime, IrwinID, IsValid, ConflictParentIrwinID,  ' \
                'ModifiedOnDateTime,  OBJECTID, CreatedBySystem, CreatedOnDateTime, ' \
                'DispatchCenterID, IsQuarantined, ControlDateTime, ContainmentDateTime, ' \
                'ModifiedBySystem, InitialResponseDateTime, FireOutDateTime'

    def get_id(self):
        if self.url_type == 'resource':
            self.id = 'IrwinRID'
        else:
            self.id = 'IrwinID'

    def get_url(self):

        # if querying irwin data, change user type to "irwin_imp" and set token url
        self.usr = 'irwinimp'

        self.token_url = 'https://{}.doi.gov/arcgis/tokens/generateToken?'.format(self.environment)
        self.url = 'https://{}.doi.gov/arcgis/rest/services/Irwin/FeatureServer/0/query'.format(self.environment)

    def get_creds(self):
        thisfile = (os.path.abspath(__file__))
        cwd = os.path.dirname(thisfile)
        irwin_ids = os.path.join(cwd, 'creds.json')

        with open(irwin_ids) as f:
            usr_data = json.load(f)

            if self.usr == 'irwinreadonly':
                self.pswd = usr_data[self.usr][self.url_type]
            else:
                self.pswd = usr_data[self.usr]
