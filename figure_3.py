import pandas as pd
from core import extract_camp_names_and_days, output_dir, data_root
import numpy as np
import matplotlib.pyplot as plt

max_move_speed = 200


def get_agent_df(location_list, days):
    file_path = f'{data_root}/agents.out.{days - 1}'
    temp_df = pd.read_csv(file_path)

    reach_camp_df = temp_df[
        (temp_df['# current location'] == temp_df[' last_location_travelled.']) & (
            ~temp_df[' is travelling']) & (temp_df[' distance travelled'] > 0) & (
            temp_df['# current location'].isin(location_list))]

    df = reach_camp_df[[' distance travelled']].copy()
    df['Days in transit'] = (df[' distance travelled'] / max_move_speed).apply(np.ceil)

    final_df = df.groupby(['Days in transit']).size().reset_index(name='No. of agents')
    final_df['Days in transit'] = pd.to_numeric(final_df['Days in transit'], downcast='signed')

    return final_df


def plot_graph(plot_data):
    plt.bar(plot_data['Days in transit'], plot_data['No. of agents'])

    plt.xlabel('Days in transit')
    plt.ylabel('No. of agents')

    # plt.show()
    plt.savefig(f'{output_dir}/figure_3_final_file_only.png', dpi=300)


if __name__ == '__main__':
    locations, total_sim_days = extract_camp_names_and_days()
    plot_data = get_agent_df(locations, total_sim_days)
    plot_graph(plot_data)
    print(f'Graphs generated in dir: {output_dir}')
