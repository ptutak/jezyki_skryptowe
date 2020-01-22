import os
import process


def test_get_files_from_folder():
    files = process.get_files_from_folder('./data')
    files = list(files)
    cwd = os.getcwd()
    assert files == [
        os.path.abspath(os.path.join(cwd, './data/sample1.csv')),
        os.path.abspath(os.path.join(cwd, './data/sample2.csv'))]


def test_get_files_dict():
    files_dict = process.get_files_dict('./data')
