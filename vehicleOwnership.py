# imported libraries
import requests

# census.gov API key
key = '2018ff1e9bad51c5f32b4198a8809febe64573d6'


def vehicle_ownership(state, county, census_tracts):
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
    tract_col = 'tract'

    url = 'https://api.census.gov/data/2019/acs/acs5' \
          '?get=%s,' \
          '%s,' \
          '%s,' \
          '%s,' \
          '%s,' \
          '%s,' \
          '%s,' \
          '%s,' \
          '%s,' \
          '%s,' \
          '%s,' \
          '%s,' \
          '%s,' \
          '%s,' \
          '%s,' \
          '%s' \
          '&for=tract:%s' \
          '&in=county:%s' \
          '&in=state:%s' \
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
    headers = {k: v for v, k in enumerate(json[0])}
    data = json[1:]
    results = []

    for row in data:
        num_households = int(row[headers[total]])
        num_owners = int(row[headers[owner_total]])
        num_renters = int(row[headers[renter_total]])

        if int(row[headers[owner_total]]) > 0:
            percent_vehicles_owner = (int(row[headers[owner_one]]) +
                                      int(row[headers[owner_two]]) +
                                      int(row[headers[owner_three]]) +
                                      int(row[headers[owner_four]]) +
                                      int(row[headers[owner_five]])) / int(row[headers[owner_total]])
        else:
            percent_vehicles_owner = None

        if int(row[headers[renter_total]]) > 0:
            percent_vehicles_renter = (int(row[headers[renter_one]]) +
                                       int(row[headers[renter_two]]) +
                                       int(row[headers[renter_three]]) +
                                       int(row[headers[renter_four]]) +
                                       int(row[headers[renter_five]])) / int(row[headers[renter_total]])
        else:
            percent_vehicles_renter = None

        if int(row[headers[total]]) > 0:
            percent_vehicles_household = (int(row[headers[owner_one]]) + int(row[headers[renter_one]]) +
                                          int(row[headers[owner_two]]) + int(row[headers[renter_two]]) +
                                          int(row[headers[owner_three]]) + int(row[headers[renter_three]]) +
                                          int(row[headers[owner_four]]) + int(row[headers[renter_four]]) +
                                          int(row[headers[owner_five]]) + int(row[headers[renter_five]])) / int(row[headers[total]])
        else:
            percent_vehicles_household = None

        if int(row[headers[owner_total]]) > 0:
            vehicles_per_owner = (int(row[headers[owner_one]]) +
                                  int(row[headers[owner_two]]) * 2 +
                                  int(row[headers[owner_three]]) * 3 +
                                  int(row[headers[owner_four]]) * 4 +
                                  int(row[headers[owner_five]]) * 5) / int(row[headers[owner_total]])
        else:
            vehicles_per_owner = None

        if int(row[headers[renter_total]]) > 0:
            vehicles_per_renter = (int(row[headers[renter_one]]) +
                                   int(row[headers[renter_two]]) * 2 +
                                   int(row[headers[renter_three]]) * 3 +
                                   int(row[headers[renter_four]]) * 4 +
                                   int(row[headers[renter_five]]) * 5) / int(row[headers[renter_total]])
        else:
            vehicles_per_renter = None

        if int(row[headers[total]]) > 0:
            vehicles_per_household = (int(row[headers[owner_one]]) + int(row[headers[renter_one]]) +
                                      int(row[headers[owner_two]]) * 2 + int(row[headers[renter_two]]) * 2 +
                                      int(row[headers[owner_three]]) * 3 + int(row[headers[renter_three]]) * 3 +
                                      int(row[headers[owner_four]]) * 4 + int(row[headers[renter_four]]) * 4 +
                                      int(row[headers[owner_five]]) * 5 + int(row[headers[renter_five]]) * 5) / int(row[headers[total]])
        else:
            vehicles_per_household = None

        ownership_data = {
            'tract': row[headers[tract_col]],
            'num_households': num_households,
            'num_owners': num_owners,
            'num_renters': num_renters,
            'percent_vehicles_household': percent_vehicles_household,
            'percent_vehicles_owner': percent_vehicles_owner,
            'percent_vehicles_renter': percent_vehicles_renter,
            'vehicles_per_household': vehicles_per_household,
            'vehicles_per_owner': vehicles_per_owner,
            'vehicles_per_renter': vehicles_per_renter,
        }

        results.append(ownership_data)

    return results
