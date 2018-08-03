# imported libraries

import requests

# census.gov API key

key = '2018ff1e9bad51c5f32b4198a8809febe64573d6'

# data set names

name = 'NAME'
total = 'B25044_001E'
owner_total = 'B25044_002E'
owner_none = 'B25044_003E'
owner_one = 'B25044_004E'
owner_two = 'B25044_005E'
owner_three = 'B25044_006E'
owner_four = 'B25044_007E'
owner_five = 'B25044_008E'
renter_total = 'B25044_009E'
renter_none = 'B25044_010E'
renter_one = 'B25044_011E'
renter_two = 'B25044_012E'
renter_three = 'B25044_013E'
renter_four = 'B25044_014E'
renter_five = 'B25044_015E'

# location info

# New York State: 36
state = '10'

# New York County: 061
# Kings County: 047
# Queens County: 081
# Bronx County: 005
# Richmond County: 085
county = '003'

census_tracts = '002100,002200,002300' # 1234.56 = 123456

# build url

url = 'https://api.census.gov/data/2016/acs/acs5'\
      '?get=%s,'\
      '%s,'\
      '%s,'\
      '%s,'\
      '%s,'\
      '%s,'\
      '%s,'\
      '%s,'\
      '%s,'\
      '%s,'\
      '%s,'\
      '%s,'\
      '%s,'\
      '%s,'\
      '%s,'\
      '%s'\
      '&for=tract:%s'\
      '&in=county:%s'\
      '&in=state:%s'\
      '&key=%s' % (
          name,
          total,
          owner_total,
          owner_none,
          owner_one,
          owner_two,
          owner_three,
          owner_four,
          owner_five,
          renter_total,
          renter_none,
          renter_one,
          renter_two,
          renter_three,
          renter_four,
          renter_five,
          census_tracts,
          county,
          state,
          key
          )

# url request

r = requests.get(url=url)

# transform data

json = r.json()

tracts = len(json)

dct = {}

for tract in range(1,tracts):
    if tract == 1:
        for row in range(len(json[0])):
            dct[json[0][row]] = json[tract][row]
    else:
        for row in range(len(json[0])):
            dct[json[0][row]] = ','.join([dct[json[0][row]],json[tract][row]])

# calculations

total_total = sum(list(map(int,dct[total].split(','))))
total_owner_total = sum(list(map(int,dct[owner_total].split(','))))
total_owner_none = sum(list(map(int,dct[owner_none].split(','))))
total_owner_one = sum(list(map(int,dct[owner_one].split(','))))
total_owner_two = sum(list(map(int,dct[owner_two].split(','))))
total_owner_three = sum(list(map(int,dct[owner_three].split(','))))
total_owner_four = sum(list(map(int,dct[owner_four].split(','))))
total_owner_five = sum(list(map(int,dct[owner_five].split(','))))
total_renter_total = sum(list(map(int,dct[renter_total].split(','))))
total_renter_none = sum(list(map(int,dct[renter_none].split(','))))
total_renter_one = sum(list(map(int,dct[renter_one].split(','))))
total_renter_two = sum(list(map(int,dct[renter_two].split(','))))
total_renter_three = sum(list(map(int,dct[renter_three].split(','))))
total_renter_four = sum(list(map(int,dct[renter_four].split(','))))
total_renter_five = sum(list(map(int,dct[renter_five].split(','))))

percent_vehicles_owner = (total_owner_one\
                     +total_owner_two\
                     +total_owner_three\
                     +total_owner_four\
                     +total_owner_five)\
                     /total_owner_total

percent_vehicles_renter = (total_renter_one\
                      +total_renter_two\
                      +total_renter_three\
                      +total_renter_four\
                      +total_renter_five)\
                      /total_renter_total

percent_vehicles_household = (total_owner_one+total_renter_one\
                         +total_owner_two+total_renter_two\
                         +total_owner_three+total_renter_three\
                         +total_owner_four+total_renter_four\
                         +total_owner_five+total_renter_five)\
                         /total_total

vehicles_per_owner = (total_owner_one\
                     +total_owner_two*2\
                     +total_owner_three*3\
                     +total_owner_four*4\
                     +total_owner_five*5)\
                     /total_owner_total

vehicles_per_renter = (total_renter_one\
                      +total_renter_two*2\
                      +total_renter_three*3\
                      +total_renter_four*4\
                      +total_renter_five*5)\
                      /total_renter_total

vehicles_per_household = (total_owner_one+total_renter_one\
                         +total_owner_two*2+total_renter_two*2\
                         +total_owner_three*3+total_renter_three*3\
                         +total_owner_four*4+total_renter_four*4\
                         +total_owner_five*5+total_renter_five*5)\
                         /total_total

# printing data to console

state = dct[name].split(', ')[2].split(',')[0]
county = dct[name].split(', ')[1]

print("State:")
print(state)
print()
print("County:")
print(county)
print()
print("Census tracts:")
for tract in census_tracts.split(','):
    tract = int(tract)
    if tract % 100 == 0:
        tract = int(tract/100)
    else:
        tract = tract/100
    print(tract)
print()
print("Owner occupied")
print("Percent vehicle ownership:", percent_vehicles_owner)
print("Vehicles per household:", vehicles_per_owner)
print()
print("Renter occupied")
print("Percent vehicle ownership:", percent_vehicles_renter)
print("Vehicles per household:", vehicles_per_renter)
print()
print("Total")
print("Percent vehicle ownership:", percent_vehicles_household)
print("Vehicles per household:", vehicles_per_household)
