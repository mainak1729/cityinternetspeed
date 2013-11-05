cityinternetspeed
=================

An web-app charting download and upload speed of ISPs in cities built on Google App Engine. The application is hosted at http://cityinternetspeed.appspot.com.

{{ city }}Data.csv files must be created from the source (http://www.netindex.com/source-data/) before running the application locally, where city is in cityList in CommonData.py. Those are csv files containing ISP name, test date, average download speed (kbps), average upload speed (kbps), number of tests analysed, average distance (miles) between the client and the server across all tests. For example,

ahmedabadData.py:

"NIB (National Internet Backbone)","2008-01-01",1549.52,237.856,272,283.735

csv files for current cityList can be found at https://drive.google.com/folderview?id=0B6GVDqnESJVsbnpaZUtxNnMwdWc&usp=sharing
