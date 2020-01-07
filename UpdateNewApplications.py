# Update New Application Permits for Dashboard Application
# https://wspdsmap.cityoftacoma.org/website/PDS/PermitDashboard/
# Script Last Updated: 2019-9-4
# Author: mmurnane
# Overwrite feature layer: https://developers.arcgis.com/python/sample-notebooks/overwriting-feature-layers/#Overwrite-the-feature-layer
# Example: https://developers.arcgis.com/python/guide/managing-your-content/
# CivicData examples: http://axtheset.github.io/bocc-civicdata/
# Login: https://developers.arcgis.com/python/guide/working-with-different-authentication-schemes/#Connecting-through-ArcGIS-Pro
# Panda Sample: https://www.kaggle.com/jboysen/quick-tutorial-flatten-nested-json-in-pandas
# Encoder: https://www.urlencoder.org/
# Works in 3.6.8

# Import libraries
from arcgis.gis import GIS  # https://esri.github.io/arcgis-python-api/apidoc/html/arcgis.gis.toc.html
from arcgis.features import FeatureLayerCollection
from datetime import date, timedelta
import time
import urllib.request
import logging
import json, csv 
import pandas as pd 
from pandas.io.json import json_normalize #package for flattening nested json in pandas df

# Variables - https://www.urlencoder.org/
#permitsResourceId = "b40a095a-e03a-4b1c-a2cb-f999b3838e0b" #Changed 9/4/2019 - http://www.civicdata.com/dataset/mapdata_v2_17662/resource/b40a095a-e03a-4b1c-a2cb-f999b3838e0b
permitsResourceId = "9474d5f7-fac8-451a-8e48-93a9ae6d6077" #Changed 1/7/2020 - http://www.civicdata.com/dataset/mapdata_v3_17678/resource/9474d5f7-fac8-451a-8e48-93a9ae6d6077

# OLD theFields = '%22Latitude%22,%22Longitude%22,%22Permit_Number%22,%22Description%22,%22Applied_Date%22,%22Current_Status%22,%22Address_Line_1%22,%22Address_Line_2%22,%22Zip%22,%22Permit_Type_Description%22,%22PermitType%22,%22Valuation%22,%22Link%22,%22Parcel_Number%22,%22Lic_Prof_Company_Name%22,%22Lic_Prof_Phone_Number%22,%22Lic_Prof_Address_Line_1%22,%22Lic_Prof_Address_Line_2%22,%22Lic_Prof_Email%22'
theFields = '%22Latitude%22,%22Longitude%22,%22Permit_Number%22,%22Description%22,%22Applied_Date%22,%22Current_Status%22,%22Address_Line_1%22,%22Address_Line_2%22,%22Zip%22,%22Permit_Type_Description%22,%22PermitType%22,%22Valuation%22,%22Link%22,%22Parcel_Number%22,%22Applicant_Name%22'
theQuery = '%22%20where%20%22Latitude%22%20%3C%3E%27%27%20and%20%22Longitude%22%20%3C%3E%20%27%27and%20%22Applied_Date%22%20%3E%3D%0A%20%27' + (date.today()-timedelta(days=30)).isoformat() + '%27%20and%20%22PermitType%22%3C%3E%27Additional%20Services%27%20and%20%22PermitType%22%3C%3E%27Code%20Compliance%27%20and%20%22PermitType%22%3C%3E%27Documents%27'
agoID = "cb01727ef47f45b7bf10406d4d3c2053"  # AGO Permit New Applications Last 30 Days - 8/7/2019

# CivicData from last 30 days (location & destination)
url = 'http://www.civicdata.com/api/3/action/datastore_search_sql?sql=SELECT%20' + theFields + '%20FROM%20%22' + permitsResourceId + theQuery
#file_json_30 = "\\\\wsitd01dev\\c$\\GADS\\website\\PDS\\PermitDashboard\\data\\PermitNewApplications30.json"  #DEV machine
#file_csv_30 = "\\\\wsitd01dev\\c$\\GADS\\website\\PDS\\PermitDashboard\\data\\PermitNewApplications30.csv"  #DEV machine
file_json_30 = "\\\\wsitd01\\c$\\GADS\\website\\PDS\\PermitDashboard\\data\\PermitNewApplications30.json"  #Production machine
file_csv_30 = "\\\\wsitd01\\c$\\GADS\\website\\PDS\\PermitDashboard\\data\\PermitNewApplications30.csv"  #Production machine

# Login to AGOL
gis = GIS("pro") # To work ArcPro must be currently logged in (can be closed).
print("")
print("Logged in as: " + gis.properties.user.username)
print("")
print("Starting time: {}".format(time.asctime( time.localtime(time.time()) )))
print("")
print("30 days before current date: ", (date.today()-timedelta(days=30)).isoformat())
print("")

try:
  print("Downloading New Permit Applications json data ...")
  urllib.request.urlretrieve(url, file_json_30) # Download the file from `url` and save it locally under `file_name`
except:
  logging.exception('\n Unexpected error with website, could not download successfully: \n')
else:
  print("Download successful!")
  print("")

  print("Converting json to csv ...")
  # Load json object - CivicData nested array
  with open(file_json_30) as f:
      d = json.load(f)
  # create flattened pandas dataframe from one nested array (result) and unpack the deeply nested array (records) 
  deepNestDF = json_normalize(data=d['result'], record_path='records')  

  # remove all '$' and ',' from Valuation field - assign the values back to the column being changed
  deepNestDF.Valuation = deepNestDF.Valuation.str.replace('$', '')
  deepNestDF.Valuation = deepNestDF.Valuation.str.replace(',', '')

  # remove YYYY- from date field
  deepNestDF.Applied_Date = deepNestDF.Applied_Date.str.slice(5)
  

  # convert to CSV
  deepNestDF.to_csv(file_csv_30, index=False)  #don't include an index column (no column header value in spreadsheet)
  print ('Done converting to CSV!')


  #Update AGOL with new CSV
  print("")
  print("Overwriting existing AGOL data ...")
  csv_item = gis.content.get(agoID) #Find New Applications
  #print(csv_item)
  csv_flayer_collection = FeatureLayerCollection.fromitem(csv_item) #Get FeatureLayerCollection
  csv_flayer_collection.manager.overwrite(file_csv_30) #Update with overwrite
  csv_flayer = csv_item.layers[0] #there is only 1 layer
  print("")
  print("New applications count: {}".format(csv_flayer.query(return_count_only=True))) #New count
  print("")
  print("Stopping time: {}".format(time.asctime( time.localtime(time.time()) )))


