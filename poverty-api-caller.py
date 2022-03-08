from urllib import request
import json
from datetime import datetime
#import matplotlib.pyplot as plt
#import numpy as np
for year in range(1995,2022):
    dataResponse=request.urlopen(f'https://api.census.gov/data/timeseries/poverty/saipe?get=SAEPOVALL_PT,SAEMHI_PT,NAME&for=county:*&time={year}', timeout=3)
    html = dataResponse.read()
    html = html.decode("utf-8")
    povertyData = json.loads(html)
    #currDate = datetime.now()
    datelist = []
    with open(f'povertyData_{year}.json', 'w') as outfile:
        json.dump(povertyData, outfile)
