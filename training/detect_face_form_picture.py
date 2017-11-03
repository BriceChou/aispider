import os
import re
import sys
import imghdr
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

def get_dir_all_file(path, list):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        temp = []
        if os.path.isdir(file_path):
            get_dir_all_file(file_path, temp)
            list.append(temp)
        elif re.match('^.*\.(jpg|gif|png|bmp)(?i)', file_path):
            list.append(file_path)


get_dir_all_file(data_path, pictures_list)

for list in pictures_list:
    i = 0
    for file_path in list:
        folder_name = os.path.dirname(file_path).split('/')[-1]
        image = load_image_file(file_path)
        locations = face_locations(
            image, number_of_times_to_upsample=0, model="hog")
        i += 1
        for location in locations:
            # Print the location of each face in this image
            top, right, bottom, left = location

            # You can access the actual face itself like this:
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            output_path = os.path.abspath(
                father_path + '/cache/' + folder_name + str(i) + '.jpg')
            pil_image.save(output_path)
