from urllib import request
import requests
import json
import csv
import time

for year in range(1995,2022):
    dataResponse=request.urlopen(f'https://api.census.gov/data/timeseries/poverty/saipe?get=SAEPOVALL_PT,SAEMHI_PT,NAME&for=county:*&time={year}', timeout=3)
    html = dataResponse.read()
    html = html.decode("utf-8")
    povertyData = json.loads(html)
    #currDate = datetime.now()
    datelist = []
    with open(f'povertyData_{year}.json', 'w') as outfile:
        json.dump(povertyData, outfile)

filename = open('countyFIPS.csv', 'r')
file = csv.DictReader(filename)
countyFIPS = []
for col in file:
    countyFIPS.append(col['FIPS'])
print(countyFIPS)

medianPropertyValues = []
for id in range(0,len(countyFIPS)):
    countyID = countyFIPS[id]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}
                                  #https://datausa.io/api/data?measure=Property%20Value,Property%20Value%20Moe&Geography=05000US01001
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
    time.sleep(0.5) #Sleep, otherwise API will throw a Captcha to prevent scraping
    print("still going "+str(id)+" "+str(len(countyFIPS)))
    fields = ['County ID', 'County Name', 'Property Value (Median)', 'Year']
with open('countyDataAllYears.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(medianPropertyValues)

#https://datausa.io/api/data?measure=Property%20Value,Property%20Value%20Moe&Geography=05000US

#WORKING LINK for Education Percentage Data:
#https://api.census.gov/data/2019/acs/acs5/profile?get=NAME,DP02_0060PE,DP02_0061PE,DP02_0062PE,DP02_0063PE,DP02_0064PE,DP02_0065PE,DP02_0066PE&for=county:*&in=state:*
#60PE - Less than 9th grade
#61 - 9th to 12th grade
#62 - High School graduate
#63 - Some College
#64 - Associate's Degree
#65 - Bachelor's Degree
#66 - Graduate or Professional Degree
# the rest of the percentage is just "other", 67 - "high school grad OR GREATER"

