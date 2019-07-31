import pandas as pd
import yaml

# Change the following absolute paths with your machines local paths
data_root = '/Users/subz/Documents/TestProjects/WorkplanScripts/mali_localhost_16'
output_dir = '/Users/subz/Documents/TestProjects/WorkplanScripts/output'


def extract_camp_names_and_days():
    location_df = pd.read_csv(f'{data_root}/out.csv')
    location_col_names = list(location_df.columns.values)
    num_days = len(list(location_df.loc[:, 'Day'].values))
    location_names = []
    for i in location_col_names:
        if " sim" in i:
            if "numAgents" not in i:
                location_names.append(' '.join(i.split()[:-1]))
    return location_names, num_days


def generate_agent_df(total_days, locations_list=[], base_location_column=' last_location_travelled.'):
    for i in range(total_days):
        file_path = f'{data_root}/agents.out.{i}'
        temp_df = pd.read_csv(file_path)
        reach_camp_df = temp_df[
            (temp_df['# current location'] != temp_df[base_location_column]) & (
                ~temp_df[' is travelling']) & (temp_df['# current location'].isin(locations_list))].copy()
        yield temp_df, reach_camp_df, i


def dict_to_yaml(filename, data_dict):
    with open(f'{output_dir}/{filename}.yml', 'w', encoding='utf8') as stream:
        yaml.dump(data_dict, stream, default_flow_style=False)
    print(f'Data written to {filename}.yml in dir: {output_dir}')
