import os
import sys

# Use the utf-8 coded format
reload(sys)
sys.setdefaultencoding('utf-8')

# Extend on our system's path and can load the other folder's file
sys.path.append('..')

import lib

# Get data folder and cache folder path
data_folder_path = os.path.abspath('../data')
cache_folder_path = os.path.abspath('../cache')

# Store the all pictures
pictures_list = []

lib.get_image_path_form_folder(data_folder_path, pictures_list)
i = lib.get_file_max_number(cache_folder_path)

for picture_list in pictures_list:
    folder_name = os.path.dirname(picture_list[0]).split('/')[-1]
    for file_path in picture_list:
        i += 1
        file_type = lib.get_file_type(file_path)

        # Move the picture into cache folder
        output_path = '{}/{}{}{}'.format(cache_folder_path,
                                         folder_name, i, file_type)
        os.rename(file_path, output_path)
        # Print new image's path
        print('%s was saved.' % output_path)
