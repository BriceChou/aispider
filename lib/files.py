import re
import os

_enable_debug = True


def _debug(str):
    if _enable_debug:
        print('%s\n' % str)


def _get_file_end_number(file_path):
    image_name = os.path.basename(file_path)

    # If there is no any number,
    # we should set the default of value with -1
    number = -1
    numbers = re.findall('\d+', image_name)
    if numbers:
        number = int(numbers[-1])
    return number


def get_file_name(file_path):
    return os.path.splitext(file_path)[0].split('/')[-1]


def get_file_type(file_path):
    return '.%s' % file_path.split('.')[-1]


def get_file_max_number(folder_path):
    temp_list = []
    get_image_path_from_folder(folder_path, temp_list, False)
    return max([_get_file_end_number(path) for path in temp_list])


def delete_files_by_type(folder_path, file_type):
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            if name.endswith(file_type):
                os.remove(os.path.join(root, name))
                _debug(os.path.join(root, name, ' was removed.'))


def get_image_path_from_folder(folder_path, store_list,
                               case_sensitive=True):
    """
    # Load all files with .jpg, .png etc type
    # If we want to load file with .jpg or .JPG type file,
    # we could change the regular expression to
    # '^.*\.(jpg|gif|png|bmp)(?i)'
    """
    pattern_string = '^.*\.(jpg|gif|png|bmp)'
    get_file_path_from_folder(folder_path, store_list,
                              pattern_string, case_sensitive)


def get_file_path_from_folder(folder_path, store_list,
                              pattern_string, case_sensitive=True):
    """ Get all folder's file
    """

    if not case_sensitive:
        pattern_string.join('(?i)')

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isdir(file_path):
            _debug(file_path.split('/')[-1])
            get_file_path_from_folder(file_path, store_list,
                                      pattern_string, case_sensitive)
        elif re.match(r'%s' % pattern_string, file_path):
            store_list.append(file_path)


def get_image_path_from_folder_group_by(folder_path, store_list,
                                        case_sensitive=True):
    """ Get all image's file and group it by folder name
    """

    pattern_string = '^.*\.(jpg|gif|png|bmp)'

    if not case_sensitive:
        pattern_string.join('(?i)')

    for file in os.listdir(folder_path):
        temp_list = []
        file_path = os.path.join(folder_path, file)
        if os.path.isdir(file_path):
            get_file_path_from_folder(file_path, temp_list,
                                      pattern_string, case_sensitive)
            if temp_list:
                store_list.append(temp_list)
        elif re.match(r'%s' % pattern_string, file_path):
            store_list.append(file_path)


def get_main_and_other_images(folder_path, main_image_list,
                              other_image_list, case_sensitive=True):
    """ Get all main image file
    """
    store_list = []
    get_image_path_from_folder(folder_path, store_list,
                               case_sensitive=True)

    # Set the main image to the first position
    for path in store_list:
        image_name = os.path.basename(path)
        if '1.jpg' == image_name:
            main_image_list.append(path)
        else:
            other_image_list.append(path)


def create_new_folder(folder_path):
    # Delete the initial blank space
    folder_path = folder_path.strip()

    # Delete end symbol '\'
    folder_path = folder_path.rstrip('\\')

    isExists = os.path.exists(folder_path)

    if not isExists:
        os.makedirs(folder_path)
        _debug('\033[0;32m%s\033[0m created success.' % folder_path)
        return True
    else:
        _debug('\033[0;32m%s\033[0m already created.' % folder_path)
        return False
