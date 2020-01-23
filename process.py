import os
import os.path
import argparse
from pandas import read_csv, ExcelWriter
from pprint import PrettyPrinter

pprint = PrettyPrinter().pprint

def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--input-folder',
        required=True
    )
    parser.add_argument(
        '-o',
        '--output-file',
        default=None,
        required=True
    )
    if args:
        return parser.parse_args(args)
    return parser.parse_args()


def get_files_from_folder(folder_name):
    full_folder_name = os.path.abspath(folder_name)
    if not os.path.isdir(full_folder_name):
        raise TypeError(f'{folder_name} is not a folder')
    root, dirnames, filenames = next(os.walk(full_folder_name))
    csv_filenames = filter(lambda x: x.endswith('.csv'), filenames)
    abs_csv_filenames = [
        os.path.abspath(os.path.join(root, filename))
        for filename in csv_filenames]
    return sorted(abs_csv_filenames)


def process_file(filename):
    return read_csv(filename, header=None, names=['node1_temp', 'node2_temp', 'node3_temp'])


def compute_mean(dataframe):
    dataframe['avg_temp'] = dataframe.mean(axis=1)


def compute_cooling_speed(dataframe):
    dataframe['cooling_rate'] = - dataframe.diff(axis=0)['avg_temp']


def add_chart(writer, sheet_name, shape):
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'categories': [sheet_name, 1, 0, shape[0] + 1, 0],
        'values': [sheet_name, 1, 4, shape[0] + 1, 4]
    })
    chart.set_x_axis({'name': 'Time'})
    chart.set_y_axis({'name': 'Average temperature', 'major_gridlines': {'visible': True}})
    chart.set_legend({'position': 'none'})

    worksheet.insert_chart('H2', chart)

    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'categories': [sheet_name, 1, 4, shape[0] + 1, 4],
        'values': [sheet_name, 1, 5, shape[0] + 1, 5]
    })
    chart.set_x_axis({'name': 'Average temperature'})
    chart.set_y_axis({'name': 'Cooling rate', 'major_gridlines': {'visible': True}})
    chart.set_legend({'position': 'none'})

    worksheet.insert_chart('H22', chart)


if __name__ == '__main__':
    args = parse_args()
    file_dict = {}
    files = get_files_from_folder(args.input_folder)

    for filename in files:
        file_dict[filename] = process_file(filename)

    for dataframe in file_dict.values():
        compute_mean(dataframe)
        compute_cooling_speed(dataframe)

    output_file = args.output_file
    if not output_file.endswith('.xlsx'):
        output_file += '.xlsx'

    with ExcelWriter(args.output_file, engine='xlsxwriter') as writer:
        for filename, dataframe in file_dict.items():
            sheet_name = os.path.basename(filename).rstrip('.csv')
            dataframe.to_excel(
                excel_writer=writer,
                sheet_name=sheet_name,
                index_label='time')
            add_chart(writer, sheet_name, dataframe.shape)
