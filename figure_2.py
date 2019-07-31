import matplotlib.pyplot as plt
import numpy as np
from core import extract_camp_names_and_days, output_dir, generate_agent_df, dict_to_yaml
from collections import namedtuple


def distance_travelled_agents(locations_list, total_days, base_location_column=' last_location_travelled.'):
    mean_distance, std_distance = [], []
    distance_max, distance_min = [], []

    for (temp_df, reach_camp_df, _) in generate_agent_df(total_days, locations_list, base_location_column):
        df_column = reach_camp_df[' distance travelled']
        mean_distance.append(float(df_column.mean()))
        std_distance.append(float(df_column.std()))
        distance_max.append(float(df_column.max()))
        distance_min.append(float(df_column.min()))

    PlotData = namedtuple('PlotData', 'mean_distance std_distance distance_max distance_min')

    return PlotData(mean_distance, std_distance, distance_max, distance_min)


def plot_graph(days_list, plot_data):
    fig, (ax1) = plt.subplots(1)
    ax1.plot(days_list, plot_data.mean_distance, linewidth=2, color=None)
    y_min = np.asarray(plot_data.mean_distance) - np.asarray(plot_data.std_distance)
    y_max = np.asarray(plot_data.mean_distance) + np.asarray(plot_data.std_distance)

    ax1.fill_between(days_list, y_max, y_min, color=None, alpha=0.5)

    ax1.set(xlabel='Days Elapsed', ylabel='Distance travelled')

    fig.savefig(f'{output_dir}/figure_2.png', dpi=300)
    # plt.show()


def plot_graph_with_old(days_list, plot_data, plot_data_old):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, constrained_layout=True)
    fig.suptitle('location of origin vs last travelled location')

    ax1.plot(days_list, plot_data_old.mean_distance, linewidth=1)
    y_min = np.asarray(plot_data_old.mean_distance) - np.asarray(plot_data_old.std_distance)
    y_max = np.asarray(plot_data_old.mean_distance) + np.asarray(plot_data_old.std_distance)
    ax1.fill_between(days_list, y_max, y_min, color=None, alpha=0.5)
    ax1.set(xlabel='Days Elapsed', ylabel='Distance travelled')

    ax2.plot(days_list, plot_data.mean_distance, linewidth=1)
    y_min = np.asarray(plot_data.mean_distance) - np.asarray(plot_data.std_distance)
    y_max = np.asarray(plot_data.mean_distance) + np.asarray(plot_data.std_distance)
    ax2.fill_between(days_list, y_max, y_min, color=None, alpha=0.5)
    ax2.set(xlabel='Days Elapsed', ylabel='Distance travelled')

    ax3.plot(days_list, plot_data_old.mean_distance, linewidth=2)
    y_min = plot_data_old.distance_min
    y_max = plot_data_old.distance_max
    ax3.fill_between(days_list, y_max, y_min, color=None, alpha=0.5)
    ax3.set(xlabel='Days Elapsed', ylabel='Distance travelled')

    ax4.plot(days_list, plot_data.mean_distance, linewidth=2)
    y_min = plot_data.distance_min
    y_max = plot_data.distance_max
    ax4.fill_between(days_list, y_max, y_min, color=None, alpha=0.5)
    ax4.set(xlabel='Days Elapsed', ylabel='Distance travelled')

    fig.savefig(f'{output_dir}/figure_2_with_old.png', dpi=300)
    # plt.show()


def generate_dict_day(position, data):
    return {
        'avg': data.mean_distance[position],
        'max': data.distance_max[position],
        'min': data.distance_min[position],
        'std': data.std_distance[position]
    }


def write_to_yml(total_days, data, data_old):
    data_dict = {}
    data_dict_old = {}
    for i in range(total_days):
        data_dict[f'Day {i}'] = generate_dict_day(i, data)
        data_dict_old[f'Day {i}'] = generate_dict_day(i, data_old)

    dict_to_yaml('figure_2_last_location', data_dict)
    dict_to_yaml('figure_2_origin_location', data_dict_old)


if __name__ == '__main__':
    locations, total_sim_days = extract_camp_names_and_days()
    days = list(range(total_sim_days))

    plot_data = distance_travelled_agents(locations, total_sim_days)

    plot_data_old = distance_travelled_agents(locations, total_sim_days, ' location of origin')

    plot_graph(days, plot_data)

    plot_graph_with_old(days, plot_data, plot_data_old)

    write_to_yml(total_sim_days, plot_data, plot_data_old)

    print(f'Graphs generated in dir: {output_dir}')
