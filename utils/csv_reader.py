import csv
from pathlib import Path


def get_path(data_file):
    cfg_file_directory = 'config'
    BASE_DIR = Path(__file__).resolve().parent.parent
    return BASE_DIR.joinpath(cfg_file_directory).joinpath(data_file)


def get_data(file_name):
    DATA_FILE = get_path(file_name)
    with open(DATA_FILE, 'r', encoding='utf8') as file:
        reader = csv.reader(file)
        next(reader)
        data = [tuple(row) for row in reader]
    return data


if __name__ == '__main__':
    print(get_data('data.csv'))
