import re
import os

_enable_debug = False


def _debug(str):
    if _enable_debug:
        print('%s\n' % str)


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


def get_file_name(file_path):
    return os.path.splitext(file_path)[0].split('/')[-1]


def get_file_type(file_path):
    return '.%s' % file_path.split('.')[-1]


def get_file_max_number(folder_path):
    temp_list = []
    _save_the_number_into_list(folder_path, temp_list)
    return max(temp_list)


def delete_files_by_type(folder_path, file_type):
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            if name.endswith(file_type):
                os.remove(os.path.join(root, name))
                _debug(os.path.join(root, name, ' was removed.'))


def get_image_path_form_folder(folder_path, store_list,
                               case_sensitive=True):
    """
    # Load all files with .jpg, .png etc type
    # If we want to load file with .jpg or .JPG type file,
    # we could change the regular expression to
    # '^.*\.(jpg|gif|png|bmp)(?i)'
    """
    pattern = re.compile(r'^.*\.(jpg|gif|png|bmp)')
    get_file_path_form_folder(folder_path, store_list,
                              pattern, case_sensitive)


def get_file_path_form_folder(folder_path, store_list,
                              pattern, case_sensitive=True):

    if not case_sensitive:
        pattern.join('(?i)')

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        temp = []
        if os.path.isdir(file_path):
            get_file_path_form_folder(file_path, temp,
                                      pattern, case_sensitive)
            store_list.append(temp)
        elif re.match(pattern, file_path):
            store_list.append(file_path)


def create_new_folder(folder_path):
    # Delete the initial blank space
    folder_path = folder_path.strip()

    # Delete end symbol '\'
    folder_path = folder_path.rstrip('\\')

    isExists = os.path.exists(folder_path)

    if not isExists:
        os.makedirs(folder_path)
        _debug('%s created success.' % folder_path)
        return True
    else:
        _debug('%s already created.' % folder_path)
        return False
