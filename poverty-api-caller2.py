from urllib import request
import requests
import json
import csv
import time

for year in range(1995, 2021):
    dataResponse=request.urlopen(f'https://api.census.gov/data/timeseries/poverty/saipe?get=SAEPOVALL_PT,SAEPOVRTALL_PT,SAEMHI_PT,NAME&for=county:*&time={year}', timeout=3)
    html = dataResponse.read()
    html = html.decode("utf-8")
    povertyData = json.loads(html)
    fields = ['All ages in Poverty, Count Estimate', 'All ages in Poverty, Rate Estimate', 'Median Household Income Estimate', 'County', 'Year', 'State ID', 'County ID']
    povertyData[0] = fields
    with open(f'data/povertyData_{year}.csv', 'w', newline='') as outfile:
        write = csv.writer(outfile)
        write.writerows(povertyData)

# fout=open("povertyData_All.csv","a")
# # first file:
# for line in open(f'data/povertyData_1995.csv'):
#     fout.write(line)
#
# # now the rest:
# for year in range(1996, 2021):
#     f = open(f'data/povertyData_{year}.csv')
#     f.next() # skip the header
#     for line in f:
#          fout.write(line)
#     f.close() # not really needed
# fout.close()