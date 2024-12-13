import csv
import os


def read_csv_as_list(directory, file_name = None):
    file_list = list_file_names(directory)
    path_separator = "\\" if os.name == 'nt' else "/"
    result = list()

    if file_name:
        file_path = directory + path_separator + file_name
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)
            result.extend(data)
    else:
        checker = False
        for file_names in file_list:
            file_path = directory + path_separator + file_names
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                reader = csv.reader(file)
                data = list(reader)

                if checker:
                    del data[0]

                checker = True
                result.extend(data)

    return result


def list_file_names(directory):
    files_in_directory = os.listdir(directory)
    return files_in_directory
