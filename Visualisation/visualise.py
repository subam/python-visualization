import pandas as pd
from core import generate_agent_df, extract_camp_names_and_days, data_root, output_dir
import folium
from folium import plugins
from pathlib import Path

# Plots the movement of single agent based on agent number and last travelled location

output_filename = 'mali_single_agent.html'


def merge_agent_df_with_coordinates(agent_df, coordinate_df):
    # Joins the dataframes based on last_location_travelled and location name from the location_df with coordinates
    df_left = pd.merge(agent_df, coordinate_df, left_on=' last_location_travelled.', right_on='#name', how='left')

    # Returns only the following columns
    df_left.drop(df_left.columns.difference(['geo_lat', 'geo_lon', 'day']), axis=1, inplace=True)
    return df_left


def generate_days_coordinates_df(total_days, location_df, camp_list, agent_number):
    coordinate_df = location_df[['#name', 'geo_lat', 'geo_lon']]
    temp_agent_df = pd.DataFrame()
    for (agents_day_df, _, i) in generate_agent_df(total_days, camp_list):
        if agent_number in agents_day_df.index:
            result_df = agents_day_df.loc[agent_number].copy()
            result_df['day'] = i
            temp_agent_df = temp_agent_df.append(result_df)

    agent_coordinates_df = merge_agent_df_with_coordinates(temp_agent_df, coordinate_df)
    return agent_coordinates_df


def plot_in_folium(location_df, agent_df, total_days):
    # Creates Map around mali with respective zoom
    plot_map = folium.Map(
        location=[16.3700359, -2.2900239],
        zoom_start=6
    )

    # Mark camps and conflict zones in map

    # Ensure you are handling floats
    location_df['geo_lat'] = location_df['geo_lat'].astype(float)
    location_df['geo_lon'] = location_df['geo_lon'].astype(float)

    camp_conflict_df = location_df.loc[
        location_df['location_type'].isin(['camp', 'conflict_zone']), ['#name', 'geo_lat', 'geo_lon',
                                                                       'location_type']]
    camp_conflict_df['marker_color'] = camp_conflict_df.apply(
        lambda row: '#00C957' if row.location_type == 'camp' else '#f9424b',
        axis=1)  # green or red based on location type

    for i in range(len(camp_conflict_df)):
        folium.CircleMarker(
            location=[camp_conflict_df.iloc[i]['geo_lat'], camp_conflict_df.iloc[i]['geo_lon']],
            popup=camp_conflict_df.iloc[i]['#name'],
            radius=20,
            color=camp_conflict_df.iloc[i]['marker_color'],  # green
            fill=True,
            fill_color=camp_conflict_df.iloc[i]['marker_color']
        ).add_to(plot_map)

    # Ensure the columns are in floats
    agent_df['geo_lat'] = agent_df['geo_lat'].astype(float)
    agent_df['geo_lon'] = agent_df['geo_lon'].astype(float)

    # Creates a list of list with latitude and longitude for each day
    # folium does not take dataframe so need to provide list input
    agent_coordinates = [
        [[row['geo_lat'], row['geo_lon']] for index, row in agent_df[agent_df['day'] == i].iterrows()]
        for i in range(int(agent_df['day'].min()), int(agent_df['day'].max() + 1))]

    # Plot it on the map
    hm = plugins.HeatMapWithTime(agent_coordinates, index=list(agent_df['day']))
    hm.add_to(plot_map)

    # save the map plot as html
    output_path = Path(output_dir).joinpath(output_filename)
    plot_map.save(str(output_path))
    print(f'Map generated: {output_path}')


if __name__ == '__main__':
    agent_number = int(input("Enter agent number: "))

    location_geocode_filePath = Path(output_dir).joinpath('location_geocode.csv')
    location_df = pd.read_csv(location_geocode_filePath)
    camp_names, num_days = extract_camp_names_and_days()

    # Check agent exists in the final day file
    final_day_df = pd.read_csv(f'{data_root}/agents.out.{num_days - 1}')

    if final_day_df.index.contains(agent_number):
        print('Agent exists')
        plot_df = generate_days_coordinates_df(num_days, location_df, camp_names, agent_number)
        plot_in_folium(location_df, plot_df, num_days)
    else:
        print('Agent not found')
