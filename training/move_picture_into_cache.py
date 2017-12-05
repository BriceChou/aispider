__author__ = 'Brice Chou'

import os
import sys

# Extend on our system's path and can load the other folder's file
sys.path.append('..')
import lib

# Use the utf-8 coded format
reload(sys)
sys.setdefaultencoding('utf-8')


def move(project_path=''):
    # Get data folder and cache folder path
    data_folder_path = os.path.abspath(project_path + 'data')
    cache_folder_path = os.path.abspath(project_path + 'cache')

    # Store the all pictures
    pictures_list = []

    lib.get_image_path_from_folder(data_folder_path, pictures_list)
    i = lib.get_file_max_number(cache_folder_path)

    for image_path in pictures_list:
        i += 1
        folder_name = lib.get_folder_name_by_file(image_path)
        file_type = lib.get_file_type(image_path)

        # Move the picture into cache folder
        output_path = '{}/{}{}.{}'.format(cache_folder_path,
                                          folder_name, i, file_type)
        os.rename(image_path, output_path)
        # Print new image's path
        print('%s was saved.' % output_path)


if __name__ == '__main__':
    move('../')
