# imported libraries

import requests

# census.gov API key

key = '2018ff1e9bad51c5f32b4198a8809febe64573d6'

# data set names

name = 'NAME'
total = 'B08006_001E'
total_car = 'B08006_002E'
car_alone = 'B08006_003E'
total_carpool = 'B08006_004E'
car_two = 'B08006_005E'
car_three = 'B08006_006E'
car_four = 'B08006_007E'
total_transit = 'B08006_008E'
bus = 'B08006_009E'
streetcar = 'B08006_010E'
subway = 'B08006_011E'
railroad = 'B08006_012E'
ferry = 'B08006_013E'
bicycle = 'B08006_014E'
walk = 'B08006_015E'
taxi = 'B08006_016E'
home = 'B08006_017E'

# location info

# New York State: 36
state = '36'

# New York County: 061
# Kings County: 047
# Queens County: 081
# Bronx County: 005
# Richmond County: 085
county = '059'

census_tracts = '405400,405500,405600,405700,405800,405900' # 1234.56 = 123456

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
      '%s,'\
      '%s,'\
      '%s'\
      '&for=tract:%s'\
      '&in=county:%s'\
      '&in=state:%s'\
      '&key=%s' % (
          name,
          total,
          total_car,
          car_alone,
          total_carpool,
          car_two,
          car_three,
          car_four,
          total_transit,
          bus,
          streetcar,
          subway,
          ferry,
          railroad,
          bicycle,
          walk,
          taxi,
          home,
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

# modal split calculations

modal_splits = {}

total_commute = sum(list(map(int,dct[total].split(','))))\
                -sum(list(map(int,dct[home].split(','))))
total_auto = sum(list(map(int,dct[total_car].split(','))))
total_bus = (sum(list(map(int,dct[bus].split(','))))\
             +sum(list(map(int,dct[streetcar].split(',')))))
total_subway = (sum(list(map(int,dct[subway].split(','))))\
                +sum(list(map(int,dct[railroad].split(',')))))
total_taxi = sum(list(map(int,dct[taxi].split(','))))

modal_splits['Auto'] = round(total_auto/total_commute,3)*100
modal_splits['Bus'] = round(total_bus/total_commute,3)*100
modal_splits['Subway/Rail'] = round(total_subway/total_commute,3)*100
modal_splits['Taxi'] = round(total_taxi/total_commute,3)*100
modal_splits['Walk/Other'] = 100-sum(modal_splits.values())

# vehicle occupancy calculations

total_alone = sum(list(map(int,dct[car_alone].split(','))))
total_two = sum(list(map(int,dct[car_two].split(','))))/2
total_three = sum(list(map(int,dct[car_three].split(','))))/3
total_four = sum(list(map(int,dct[car_four].split(','))))/4

veh_occ = round(total_auto/(total_alone+total_two+total_three+total_four),2)

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
print("Modal split:")
for key, value in modal_splits.items():
    print(key + ':', '%.1f' % round(value,1))
print()
print("Vehicle occupancy:")
print('%.2f' % veh_occ)
