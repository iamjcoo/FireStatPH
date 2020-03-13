import csv
import json
import re
import codecs
import random

data = 'BFP_FIreIncidents2012-2016.csv'
rlist=[]
lyear=[]
year=dict()
hey=dict()

labels = ['PSGC','REGION','PROVINCE_FIRE_DISTRICT','CONGRESSIONAL_DISTRICT','CITY_MUNICIPALITY','YEAR','INCIDENTS','INJURIES','DEATHS','ESTIMATED_DAMAGES']
with open(data, 'r') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=labels)
    for row in reader:
        rlist.append(row)
for x in rlist:
    if x['YEAR'] not in lyear:
        lyear.append(x['YEAR'])
    else:
        continue

print(rlist)
