from pathlib import Path
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from core import output_dir, data_root

'''
Locates the location.csv file in the input directory
Uses the geopy python package to get the coordinates for the location names
It uses the current one available in the file if it cannot find the coordinates 
The delay has been put to 2 seconds but can be put to 1 as to much request to the api can cause it to timeout
or some other error because of openstreetmap limitation
'''

output_filename = 'location_geocode.csv'


def generate_location_coordinates():
    location_file_path = Path(data_root).joinpath('input_csv', 'locations.csv')

    df = pd.read_csv(location_file_path)

    df['query_location'] = df.apply(lambda row: row['#name'] + ', ' + row['country'], axis=1)

    geolocator = Nominatim(user_agent='coordinates-mali')

    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
    df['location'] = df['query_location'].apply(geocode)
    df['geo_lon'] = df['location'].apply(lambda loc: loc.longitude if loc else None)
    df['geo_lat'] = df['location'].apply(lambda loc: loc.latitude if loc else None)

    df['geo_lon'].fillna(df['lon'], inplace=True)
    df['geo_lat'].fillna(df['lat'], inplace=True)

    result_df = df[['#name', 'country', 'lat', 'lon', 'geo_lat', 'geo_lon', 'location_type']]

    output_path = Path(output_dir).joinpath(output_filename)
    result_df.to_csv(output_path, index=False)
    print(f'{output_filename} generated in {output_path}')


if __name__ == '__main__':
    generate_location_coordinates()
