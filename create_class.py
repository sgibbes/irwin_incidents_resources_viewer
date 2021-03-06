'''

for reference:
input is:
- irwin data
- irwin test
- irwin oat

'''
import json
import sys


class QueryType:

    def __init__(self, url_type):

        self.url_type = url_type

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

        environ_dict = {'api': 'irwin', 'oat': 'irwinoat', 'test': 'irwint', 'oat next': 'irwinoat'}

        if self.url_type == 'irwin data':
            # if querying irwin data, change user type to "irwin_imp" and set token url
            self.usr = 'irwin_imp'
            self.token_url = 'https://www.arcgis.com/sharing/generatetoken?expiration=120&referer=localhost&f=json'

            self.url = 'https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Incidents/FeatureServer/0/query'

        if self.url_type == 'api':
            self.url = 'https://{}.doi.gov/arcgis/rest/services/Irwin/FeatureServer/0/query'.format(
                environ_dict[self.url_type])
            self.usr = 'irwinreadonly'
            self.token_url = 'https://{}.doi.gov/arcgis/tokens/generateToken?'.format(environ_dict[self.url_type])

        if self.url_type == 'oat':
            self.usr = 'irwinreadonly'
            self.url = 'https://{}.doi.gov/arcgis/rest/services/Irwin/FeatureServer/0/query'.format(environ_dict[self.url_type])
            self.token_url = 'https://{}.doi.gov/arcgis/tokens/generateToken?'.format(environ_dict[self.url_type])

        if self.url_type == 'test':
            self.usr = 'irwinreadonly'
            self.token_url = 'https://{}.doi.gov/arcgis/tokens/generateToken?'.format(environ_dict[self.url_type])
            self.url = 'https://{}.doi.gov/arcgis/rest/services/Irwin/FeatureServer/0/query'.format(environ_dict[self.url_type])

        if self.url_type == 'oat next':

            self.usr = 'irwinimp'
            self.url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Irwin/FeatureServer/0/query'
            self.token_url = 'https://irwinoat.doi.gov/arcgis/tokens/generateToken?'

        if self.url_type == 'resource':
            self.usr = 'irwinimp'
            self.url = 'https://irwinoat.doi.gov/arcgis/rest/services/next/Resource/FeatureServer/0/query'
            self.token_url = 'https://irwinoat.doi.gov/arcgis/tokens/generateToken?'

    def get_creds(self):

        irwin_ids = 'creds.json'

        with open(irwin_ids) as f:
            usr_data = json.load(f)

            if self.usr == 'irwinreadonly':
                self.pswd = usr_data[self.usr][self.url_type]
            else:
                self.pswd = usr_data[self.usr]
