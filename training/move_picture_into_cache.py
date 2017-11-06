import os
import re
import sys
import shutil

# Extend on our system's path and can load the other folder's file
sys.path.append('..')

from lib.utils import *

# Get current file's path
pwd = os.getcwd()

# Get project's path
father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + '.')

# Get data's path
data_path = os.path.abspath(father_path + '/data')

cache_path = os.path.abspath(father_path + '/cache')

# Remove the cache folder and all files
print(cache_path + ' folder has been removed.')
shutil.rmtree(cache_path)

# Create the cache folder again
print(cache_path + ' folder was created.')
os.mkdir(cache_path)

# Store the all pictures
pictures_list = []


def get_file_type(path):
    return path.split('.')[-1]


def get_file_path_form_dir(path, store_list):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        temp = []
        if os.path.isdir(file_path):
            get_file_path_form_dir(file_path, temp)
            store_list.append(temp)
        elif re.match('^.*\.(jpg|gif|png|bmp)', file_path):
            store_list.append(file_path)


get_file_path_form_dir(data_path, pictures_list)


for picture_list in pictures_list:
    i = 0
    folder_name = os.path.dirname(picture_list[0]).split('/')[-1]
    for file_path in picture_list:
        i += 1
        file_type = '.' + get_file_type(file_path)

        # Move the picture into cache folder
        output_path = os.path.abspath(
            father_path + '/cache/' + folder_name + str(i) + file_type)
        os.rename(file_path, output_path)

        # Print new image's path
        print(output_path + ' was saved.')
