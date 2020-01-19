import os

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
