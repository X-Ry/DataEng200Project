from urllib import request
import requests
import json
import csv
import time

# ----- Poverty + Income Data -----
# Uses Census API to gather Poverty & Household Income Data by Year and County,
# appends the Full County ID to each row of data,
# and stores it in the povertyData_AllYears.csv file

# SAEPOVALL_PT = All ages in Poverty, Count Estimate
# SAEPOVRTALL_PT = All ages in Poverty, Rate Estimate
# SAEMHI_PT = Median Household Income Estimate

print("Gather Poverty + Income Data")
with open(f'data/povertyData_AllYears.csv', 'w', newline='') as outfile:
    write = csv.writer(outfile)
    for year in range(1995, 2021):
        print(year)
        dataResponse=request.urlopen(f'https://api.census.gov/data/timeseries/poverty/saipe?get=SAEPOVALL_PT,SAEPOVRTALL_PT,SAEMHI_PT,NAME&for=county:*&time={year}', timeout=30)
        html = dataResponse.read()
        html = html.decode("utf-8")
        povertyData = json.loads(html)
        fields = ['All ages in Poverty, Count Estimate', 'All ages in Poverty, Rate Estimate', 'Median Household Income Estimate', 'County', 'Year', 'State ID', 'County ID', 'Full County ID']
        #Add the Full County ID
        for p in povertyData:
            p.append(p[5]+p[6])
        povertyData[0] = fields
        write.writerows(povertyData)

# ----- Education Data -----
# Uses Census API to gather Educational Attainment Data by Year and County,
# appends the Full County ID and Year to each row of data,
# and stores it in the educationData_AllYears.csv file

# DP02_0060PE - Less than 9th grade
# DP02_0061PE - 9th to 12th grade
# DP02_0062PE - High School graduate
# DP02_0063PE - Some College
# DP02_0064PE - Associate's Degree
# DP02_0065PE - Bachelor's Degree
# DP02_0066PE - Graduate or Professional Degree

print("Gather Education Data")
with open(f'data/educationData_AllYears.csv', 'w', newline='') as outfile:
    write = csv.writer(outfile)
    for year in range(2009, 2020):
        dataResponse = request.urlopen(
            f'https://api.census.gov/data/{year}/acs/acs5/profile?get=NAME,DP02_0060PE,DP02_0061PE,DP02_0062PE,DP02_0063PE,DP02_0064PE,DP02_0065PE,DP02_0066PE&for=county:*&in=state:*',
            timeout=3)
        html = dataResponse.read()
        html = html.decode("utf-8")
        educationData = json.loads(html)
        fields = ['County', 'Less than 9th Grade', '9th to 12th Grade', 'High School Graduate', 'Some College',
                  'Associates Degree', 'Bachelors Degree', 'Graduate or Professional Degree', 'State ID',
                  'County ID', 'Full County ID', 'Year']
        # Add the Full County ID
        for p in educationData:
            p.append(p[8] + p[9])
            p.append(str(year))
        educationData[0] = fields
        write.writerows(educationData)

# ----- Unemployment Data -----
# Uses Census API to gather Unemployment Rate Data by Year and County,
# appends the Full County ID and Year to each row of data,
# and stores it in the educationData_AllYears.csv file

# DP03_0009PE = Unemployment Rate Percentage

print("Gather Unemployment Data")
with open(f'data/unemploymentData_AllYears.csv', 'w', newline='') as outfile:
    write = csv.writer(outfile)
    for year in range(2009, 2020):
        dataResponse=request.urlopen(f'https://api.census.gov/data/{year}/acs/acs5/profile?get=NAME,DP03_0009PE&for=county:*&in=state:*', timeout=3)
        html = dataResponse.read()
        html = html.decode("utf-8")
        unemploymentData = json.loads(html)
        fields = ['County', 'Unemployment Rate Percentage', 'State ID', 'County ID','Full County ID','Year']
        # Add the Full County ID
        for p in unemploymentData:
            p.append(p[2] + p[3])
            p.append(str(year))
        unemploymentData[0] = fields
        write.writerows(unemploymentData)

# ----- Loading County FIPS Data -----
# Loads a list of all USA County FIPS,
# which is used to collect Property Value Data.

print("Load County FIPS Data")
filename = open('data/countyFIPS.csv', 'r')
file = csv.DictReader(filename)
countyFIPS = []
for col in file:
    countyFIPS.append(col['FIPS'])

# ----- Property Value Data -----
# Uses DataUSA API to gather Yearly Median Property Value Data by County,
# saves data in a dictionary,
# and writes data to the countyPropertyValueDataAllYears_Uncleaned.csv file

print("Gather Property Value Data")
medianPropertyValues = []
for id in range(0,len(countyFIPS)):
    countyID = countyFIPS[id]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}
    dataResponse=requests.get('https://datausa.io/api/data?measure=Property%20Value,Property%20Value%20Moe&Geography=05000US'+countyID, timeout=300, headers = headers)
    idData = dataResponse.json()
    for idYear in idData['data']:
        yearValue = idYear['Year']
        propertyValue = idYear['Property Value']
        if 'Geography' in idYear:
            geography = idYear['Geography']
        else:
            geography = 'N/A'
        medianPropertyValues.append([countyID, geography, propertyValue, yearValue])
    time.sleep(0.5)
    print("Collecting Data - "+str(id)+" out of "+str(len(countyFIPS)))
    fields = ['Full County ID', 'County Name', 'Property Value (Median)', 'Year']
with open('data/countyPropertyValueDataAllYears_Uncleaned.csv', 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(medianPropertyValues)
