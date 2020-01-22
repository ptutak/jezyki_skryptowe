import os
import argparse
from pandas import read_csv
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
    return read_csv(filename, header=None)

if __name__ == '__main__':
    args = parse_args()
    file_dict = {}
    files = get_files_from_folder(args.input_folder)
    for filename in files:
        file_dict[filename] = process_file(filename)

    pprint(file_dict)
