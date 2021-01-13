## Craig O'Donnell
## Census Transportation Data
## 12/19/2018

# imported libraries
import csv
import time
import requests
import json
import pandas as pd
from vehicleOwnership import vehicle_ownership

# census.gov API key
key = '2018ff1e9bad51c5f32b4198a8809febe64573d6'

# data set name(s)
name = 'NAME'

# location info

# New York State: 36
state = '36'

# New York County: 061
# Kings County: 047
# Queens County: 081
# Bronx County: 005
# Richmond County: 085
counties = ['061', '047', '081', '005', '085']
county_names = {'061': 'New York',
                '047': 'Kings',
                '081': 'Queens',
                '005': 'Bronx',
                '085': 'Richmond'}

outputFile = 'data/NYC_Vehicle_Ownership_2019.csv'

def get_county_tracts(state, county):

    census_tracts = '*' # 1234.56 = 123456

    # build url
    url = 'https://api.census.gov/data/2019/acs/acs5'\
          '?get=%s'\
          '&for=tract:%s'\
          '&in=county:%s'\
          '&in=state:%s'\
          '&key=%s' % (
              name,
              census_tracts,
              county,
              state,
              key
              )

    # url request
    r = requests.get(url=url)

    # transform data
    json_response = r.json()
    json_str = json.dumps(json_response)

    # pandas
    df = pd.read_json(json_str)
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    tracts = df.tract

    return tracts

def analyze_tracts(county, tracts):

    startTime = time.time()

    county_name = county_names[county]
    
    print("Pulling data for %s county." % county_name)
    
    data = []
    county_tracts = ','.join(tracts)
    # try:
    results = vehicle_ownership(state, county, county_tracts)
    for row in results:
        tract = row['tract']
        percent_vehicles_owner = row['percent_vehicles_owner']
        percent_vehicles_renter = row['percent_vehicles_renter']
        percent_vehicles_household = row['percent_vehicles_household']
        vehicles_per_owner = row['vehicles_per_owner']
        vehicles_per_renter = row['vehicles_per_renter']
        vehicles_per_household = row['vehicles_per_household']
        data.append([county_name,
                     tract,
                     percent_vehicles_owner,
                     percent_vehicles_renter,
                     percent_vehicles_household,
                     vehicles_per_owner,
                     vehicles_per_renter,
                     vehicles_per_household])
    # except Exception as e:
    #     print('Error for county %s' % county, e)

    runTime = time.time() - startTime

    print("%i tracts analyzed in %f seconds." % (len(tracts), runTime))
        
    return data

def write_to_csv(data, outputFile):

    # writes data to .csv file for use in other programs    
    with open(outputFile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)



all_data = [
    [
        'county',
        'tract',
        'percent_vehicles_owner',
        'percent_vehicles_renter',
        'percent_vehicles_household',
        'vehicles_per_owner',
        'vehicles_per_renter',
        'vehicles_per_household'
     ]
]

for county in counties:
    tracts = get_county_tracts(state, county)
    county_data = analyze_tracts(county, tracts)
    all_data.extend(county_data)

write_to_csv(all_data, outputFile)
print('Output written to %s' % outputFile)
