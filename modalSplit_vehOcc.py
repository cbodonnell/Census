import requests

# census.gov API key
key = '2018ff1e9bad51c5f32b4198a8809febe64573d6'


def modalSplit_vehOcc(state, county, census_tracts):

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
    subway = 'B08006_010E'
    railroad = 'B08006_011E'
    streetcar = 'B08006_012E'
    ferry = 'B08006_013E'
    bicycle = 'B08006_014E'
    walk = 'B08006_015E'
    taxi = 'B08006_016E'
    home = 'B08006_017E'
    tract_col = 'tract'

    # build url
    url = 'https://api.census.gov/data/2019/acs/acs5'\
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
              subway,
              railroad,
              streetcar,
              ferry,
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
    headers = {k: v for v, k in enumerate(json[0])}
    data = json[1:]
    results = []
    for row in data:
        tract = row[headers[tract_col]]
        modal_splits = {}
        total_commute = int(row[headers[total]]) - int(row[headers[home]])
        total_auto = int(row[headers[total_car]])
        total_bus = int(row[headers[bus]]) + int(row[headers[streetcar]])
        total_subway = int(row[headers[subway]]) + int(row[headers[railroad]])
        total_taxi = int(row[headers[taxi]])
        try:
            modal_splits['Auto'] = round(total_auto / total_commute, 3)
            modal_splits['Bus'] = round(total_bus / total_commute, 3)
            modal_splits['Subway/Rail'] = round(total_subway / total_commute, 3)
            modal_splits['Taxi'] = round(total_taxi / total_commute, 3)
            modal_splits['Walk/Other'] = round(1 - sum(modal_splits.values()), 3)
        except ZeroDivisionError:
            modal_splits['Auto'] = None
            modal_splits['Bus'] = None
            modal_splits['Subway/Rail'] = None
            modal_splits['Taxi'] = None
            modal_splits['Walk/Other'] = None

        # vehicle occupancy calculations
        total_alone = int(row[headers[car_alone]])
        total_two = int(row[headers[car_two]]) / 2
        total_three = int(row[headers[car_three]]) / 3
        total_four = int(row[headers[car_four]]) / 4

        try:
            veh_occ = round(total_auto / (total_alone + total_two + total_three + total_four), 2)
        except ZeroDivisionError:
            veh_occ = None
        result = {
            'tract': tract,
            'total_commute': total_commute,
            'modal_splits': modal_splits,
            'total_auto': total_auto,
            'veh_occ': veh_occ
        }
        results.append(result)
    return results
