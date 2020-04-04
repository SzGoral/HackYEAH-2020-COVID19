import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import io
from PIL import Image
from . import electrode_matrix
# import electrode_matrix
from collections import defaultdict
from pprint import pprint
import math as m

BEETWEEN_ELEC_X = 60
BEETWEEN_ELEC_Y = 60
GRID_CONST = 2
MAKE_EVEN = 2
Y_AXIS_TRESH = [-5, 5]
X_AXIS_START = 0
X_AXIS_END = 100


def plot_pxmy_to_bytes(paths: list, ele_from, ele_to):

    fig = plt.figure(figsize=(17, 17))
    for path in paths:
        for el in range(ele_from, ele_to + 1):
            with open(path, 'rb') as f:
                data = np.fromfile(f, dtype=np.dtype('<i2'))
            data_traces = data[1000:].reshape(data[0], data[1], data[2], order='F')

            data = np.squeeze(data_traces[:, el - 1, :])

            plt.plot(np.transpose(data), 'r')

    plt.title("test")

    return get_bytes(fig)


def plot_pxmy_without_neighbours(paths: list, main_electrode, movie_number, y_axis_min=None, y_axis_max=None,
                                                          x_axis_min=0, x_axis_max=100):
    y_axis_calc = list()
    if y_axis_min or y_axis_max is None:
        for path in paths:
            for el in range(main_electrode + 1):
                with open(path, 'rb') as f:
                    data = np.fromfile(f, dtype=np.dtype('<i2'))
                data_traces = data[1000:].reshape(data[0], data[1], data[2], order='F')
                data = np.squeeze(data_traces[:, el - 1, :])
                data = np.transpose(data)
                y_axis_calc.append(data.min())
                y_axis_calc.append(data.max())

    if y_axis_min == None:
        y_axis_min = min(y_axis_calc)
    if y_axis_max == None:
        y_axis_max = max(y_axis_calc)
    if x_axis_min == None:
        x_axis_min = X_AXIS_START
    if x_axis_max == None:
        x_axis_max = X_AXIS_END

    fig = plt.figure(figsize=(17, 17))

    for path in paths:
        with open(path, 'rb') as f:
            data = np.fromfile(f, dtype=np.dtype('<i2'))
        data_traces = data[1000:].reshape(data[0], data[1], data[2], order='F')
        data = np.squeeze(data_traces[:, main_electrode - 1, :])
        a = np.transpose(data)

        plt.plot(np.transpose(data), 'r')
        y_axis_tresh = int(0.05 * (y_axis_max - y_axis_min))
        plt.ylim(y_axis_min - y_axis_tresh, y_axis_max + y_axis_tresh)
        x_axis_tresh = int(0.05 * (x_axis_max - x_axis_min))
        plt.xlim(x_axis_min - x_axis_tresh, x_axis_max + x_axis_tresh)
        plt.title(f'electrode: {main_electrode}, movie number: {movie_number}')
        plt.xlabel('time')
        plt.ylabel('A')

    # fig.tight_layout()
    # fig.savefig('demo2.png', bbox_inches='tight')
    return get_bytes(fig)


def plot_pxmy_and_neighbours(paths: list, main_electrode, movie_number, y_axis_min=None, y_axis_max=None,
                                                          x_axis_min=0, x_axis_max=100):
    matrix = electrode_matrix.ElectrodeMatrix('retina/electrodes.csv')
    main_electrode_coord = matrix.get_coord_for_pattern(main_electrode)
    neighbours = matrix.get_neighbours(main_electrode)

    elec_dict = {ele: matrix.get_coord_for_pattern(ele) for ele in neighbours}
    elec_dict[main_electrode] = main_electrode_coord

    uniq_x = [v[0] for k, v in elec_dict.items()]
    uniq_x = set(uniq_x)
    uniq_y = [v[1] for k, v in elec_dict.items()]
    uniq_y = set(uniq_y)

    minX = min(elec_dict.items(), key=lambda x: x[1][0])[1][0]
    maxX = max(elec_dict.items(), key=lambda x: x[1][0])[1][0]
    minY = min(elec_dict.items(), key=lambda x: x[1][1])[1][1]
    maxY = max(elec_dict.items(), key=lambda x: x[1][1])[1][1]

    offset_col = len(uniq_x) - 1
    if len(uniq_y) == 3:
        offset_raw = len(uniq_y) + 1
    else:
        offset_raw = len(uniq_y)
    plots_in_col = m.ceil((np.abs(maxX - minX)) / BEETWEEN_ELEC_X + 1)
    plots_in_row = m.ceil((np.abs(maxY - minY)) / BEETWEEN_ELEC_Y + 1)

    grid_rows = 2 * plots_in_row
    grid_cols = 2 * plots_in_col

    plot_height = int(grid_rows / plots_in_row)
    plot_length = int(grid_cols / plots_in_col)

    max_plots = max(grid_rows, grid_cols)

    elec_to_plot = defaultdict(list)
    for k, v in elec_dict.items():
        elec_to_plot[k].append(np.abs((elec_dict[k][0] - minX) * offset_col / (maxX - minX)))
        elec_to_plot[k].append(np.abs((elec_dict[k][1] - maxY) * offset_raw / (maxY - minY)))

    y_axis_calc = list()
    if y_axis_min or y_axis_max is None:
        for path in paths:
            for i, (k, v) in enumerate(elec_to_plot.items()):
                with open(path, 'rb') as f:
                    data = np.fromfile(f, dtype=np.dtype('<i2'))
                data_traces = data[1000:].reshape(data[0], data[1], data[2], order='F')
                data = np.squeeze(data_traces[:, k - 1, :])
                data = np.transpose(data)
                y_axis_calc.append(data.min())
                y_axis_calc.append(data.max())

    if y_axis_min == None:
        y_axis_min = min(y_axis_calc)
    if y_axis_max == None:
        y_axis_max = max(y_axis_calc)
    if x_axis_min == None:
        x_axis_min = X_AXIS_START
    if x_axis_max == None:
        x_axis_max = X_AXIS_END

    fig = plt.figure(figsize=(17, 17))
    gs = gridspec.GridSpec(nrows=max_plots, ncols=max_plots, wspace=1, hspace=0.5)

    for path in paths:
        for i, (k, v) in enumerate(elec_to_plot.items()):
            with open(path, 'rb') as f:
                data = np.fromfile(f, dtype=np.dtype('<i2'))
            data_traces = data[1000:].reshape(data[0], data[1], data[2], order='F')
            data = np.squeeze(data_traces[:, k - 1, :])
            a = np.transpose(data)

            axs = fig.add_subplot(gs[int(v[1]):int(v[1]) + plot_height, int(v[0]):int(v[0]) + plot_length])
            axs.plot(np.transpose(data), 'r')
            y_axis_tresh = int(0.05 * (y_axis_max - y_axis_min))
            axs.set_ylim(y_axis_min - y_axis_tresh, y_axis_max + y_axis_tresh)
            x_axis_tresh = int(0.05 * (x_axis_max - x_axis_min))
            axs.set_xlim(x_axis_min - x_axis_tresh, x_axis_max + x_axis_tresh)
            axs.set_title(f'electrode: {k}, movie number: {movie_number}')
            axs.set(xlabel='time', ylabel='A')

    # fig.tight_layout()
    # fig.savefig('demo.png', bbox_inches='tight')
    return get_bytes(fig)


def get_bytes(plt):
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_value = buf.getvalue()
    buf.close()
    plt.clf()
    return plot_value


if __name__ == "__main__":

    data = plot_pxmy_and_neighbours([r'/home/szgoral/magisterka/testdata/2015-04-14-0/data001/p26/p26_m181'], 34)
    data2 = plot_pxmy_without_neighbours([r'/home/szgoral/magisterka/testdata/2015-04-14-0/data001/p26/p26_m181'], 26)
