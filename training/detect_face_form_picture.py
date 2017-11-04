import os
import re
import sys
from PIL import Image

# Extend on our system's path and can load the other folder's file
sys.path.append('..')

from lib.utils import *

# Get current file's path
pwd = os.getcwd()

# Get project's path
father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + '.')

# Get data's path
data_path = os.path.abspath(father_path + '/data')

pictures_list = []


def get_file_path_form_dir(path, list):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        temp = []
        if os.path.isdir(file_path):
            get_file_path_form_dir(file_path, temp)
            list.append(temp)
        elif re.match('^.*\.(jpg|gif|png|bmp)(?i)', file_path):
            list.append(file_path)


get_file_path_form_dir(data_path, pictures_list)

for list in pictures_list:
    i = 0
    for file_path in list:
        folder_name = os.path.dirname(file_path).split('/')[-1]
        image = load_image_file(file_path)
        locations = face_locations(
            image, number_of_times_to_upsample=0, model="hog")
        i += 1
        for location in locations:
            top, right, bottom, left = location
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            output_path = os.path.abspath(
                father_path + '/cache/' + folder_name + str(i) + '.jpg')
            pil_image.save(output_path)
