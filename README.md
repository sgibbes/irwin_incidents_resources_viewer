# irwin_incidents_resources_viewer
This README applies to the script "query_incdients.py" and "resources.py". 

Use this tool to query the Irwin Incidents and Irwin Resources endpoints. This tool is currently under development.

Other files in this repo are also under development.

Initial Setup:
1. Create a file called creds.json. This can be done in a text editor. Just change the extention from .txt to .json. Accept the warning that might come up.
2. Edit the creds file to look like: 
{"yourusername": "yourpassword"}
Where you replace each with the username/password you use to access the Irwin ArcGIS account

To Query Incidents:
1. Run python query_incidents.py
2. Enter answers when prompted\
    a. Endpoint Type: irwin data, api, oat, test, oat next\
    b. IrwinID: format as xxxx-xxxx etc\
    c. PooState
3. If no answers are provided, the query returns all incidents

To Query Resources
1. Run python resources.py
2. Enter answers when prompted\
a. 
