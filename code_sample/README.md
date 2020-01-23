Sample code for downloading resources data from IRWIN OAT/NEXT 

Replace text with your username/password here:
`code_sample/main.py:8`

Run the code: `python main.py`

The code will get the token, then query the specific table (read below to change that table).

The script is initially set up to query a specific set of resources. If this runs without error, 
remove the additional query params so that it reads `1=1` (`code_sample/main.py:19`)

The nature of this script is to download ALL records in a particular table. 
Since the REST endpoint limits the number of records returned to 2,000, an iterator-type looping is used to page the endpoint. 
This is done using the parameter resultOffset

Each iteration collects 2,000 records. These are appended to a dictionary in memory.

When the data element 'exceededTransferLimit' is False, the iterating ends.

The dictionary is converted to a pandas dataframe (or can be run without pandas, see below), and then written to a csv which is saved in this directory.

- To change the output csv file name, edit this line: `code_sample/main.py:25`


- To change the table that is queried, edit the endpoint url: `code_sample/main.py:15`. Replace the "0" following FeatureServer with a table number.
Reference the REST endpoint for table indexes.
(https://services1.arcgis.com/Hp6G80Pky0om7QvQ/ArcGIS/rest/services/[OAT_NEXT]_Resources_VIEW_(Read_Only)/FeatureServer)

- To change the where clause, edit the where variable: `code_sample/main.py:19`

- If you do not have pandas, change this line: `code_sample.util.response_to_dict` and replace `response_to_dict`
 with `response_to_dict_nopd`. Then remove the pandas import line (`code_sample/util.py:5`). The alternative "csv" library is used in its place. However this might be slower to write to.




