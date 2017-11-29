import re
import os


def _save_the_number_into_list(folder_path, store_list):
    """
    To save all file's number and find the max number from this list.

    This function only suitable for LINUX system.

    Args:

    Returns:
    """
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        temp_list = []
        if os.path.isdir(file_path):
            _save_the_number_into_list(file_path, temp_list)
            store_list.append(temp_list)
        elif re.match('^.*\.(jpg|gif|png|bmp)(?i)', file_path):
            image_name = os.path.basename(file_path)
            number = 1
            numbers = re.findall('\d+', image_name)
            if len(numbers):
                number = int(numbers[-1])
            store_list.append(number)


def get_file_max_number(folder_path):
    temp_list = []
    _save_the_number_into_list(folder_path, temp_list)
    return max(temp_list)
