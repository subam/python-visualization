import matplotlib.pyplot as plt
from core import extract_camp_names_and_days, output_dir, generate_agent_df, dict_to_yaml
from collections import namedtuple


def agents_who_reach_camp(locations_list, total_days, base_location_column=' last_location_travelled.'):
    percent_agents_list, total_agent_list, successful_agent_list = [], [], []

    for (temp_df, reach_camp_df, _) in generate_agent_df(total_days, locations_list, base_location_column):
        total_agent_list.append(len(temp_df.index))
        successful_agent_list.append(len(reach_camp_df.index))

        percent_agent_reach_camp = (len(reach_camp_df.index) / len(temp_df.index)) * 100
        percent_agents_list.append(percent_agent_reach_camp)

    PlotData = namedtuple('PlotData', 'percent_agents_list successful_agent_list total_agent_list')

    return PlotData(percent_agents_list, successful_agent_list, total_agent_list)


def plot_graphs(days_list, plot_data):
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(days_list, plot_data.percent_agents_list)
    ax1.set(xlabel='Days Elapsed', ylabel='% of successful travel')

    ax2.plot(days_list, plot_data.total_agent_list, label='Total agents')
    ax2.plot(days_list, plot_data.successful_agent_list, label='Agents that reached camp')
    ax2.legend()
    ax2.set(xlabel='Days Elapsed', ylabel='No. of agents')

    fig.subplots_adjust(hspace=.5)

    fig.savefig(f'{output_dir}/figure_1.png', dpi=300)
    # plt.show()


def plot_graph_with_old(days_list, plot_data, plot_data_old):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, constrained_layout=True)
    fig.suptitle('location of origin vs last travelled location')

    ax1.plot(days_list, plot_data_old.percent_agents_list)
    ax1.set(xlabel='Days Elapsed', ylabel='% of successful travel')

    ax2.plot(days_list, plot_data.percent_agents_list)
    ax2.set(xlabel='Days Elapsed', ylabel='% of successful travel')

    ax3.plot(days_list, plot_data_old.total_agent_list, label='Total agents')
    ax3.plot(days_list, plot_data_old.successful_agent_list, label='Agents that reached camp')
    ax3.legend(fontsize='x-small')
    ax3.set(xlabel='Days Elapsed', ylabel='No. of agents')

    ax4.plot(days_list, plot_data.total_agent_list, label='Total agents')
    ax4.plot(days_list, plot_data.successful_agent_list, label='Agents that reached camp')
    ax4.legend(fontsize='x-small')
    ax4.set(xlabel='Days Elapsed', ylabel='No. of agents')

    fig.savefig(f'{output_dir}/figure_1_with_old.png', dpi=300)
    # plt.show()


def generate_dict_day(position, data):
    return {
        'percentage_agents_reach_camp': data.percent_agents_list[position],
        'number_agent_reach_camp': data.successful_agent_list[position],
        'total_agents': data.total_agent_list[position]
    }


def write_to_yaml(total_days, data, data_old):
    data_dict = {}
    data_dict_old = {}
    for i in range(total_days):
        data_dict[f'Day {i}'] = generate_dict_day(i, data)
        data_dict_old[f'Day {i}'] = generate_dict_day(i, data_old)

    dict_to_yaml('figure_1_last_location', data_dict)
    dict_to_yaml('figure_1_origin_location', data_dict_old)


if __name__ == '__main__':
    locations, total_sim_days = extract_camp_names_and_days()
    plot_data = agents_who_reach_camp(locations, total_sim_days)

    # using old approach
    plot_data_old = agents_who_reach_camp(locations,
                                          total_sim_days,
                                          ' location of origin')

    days = list(range(total_sim_days))

    plot_graphs(days, plot_data)

    plot_graph_with_old(days, plot_data, plot_data_old)

    write_to_yaml(total_sim_days, plot_data, plot_data_old)

    print(f'Graphs generated in dir: {output_dir}')
