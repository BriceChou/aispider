import os
import re
import sys
import shutil
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

cache_path = os.path.abspath(father_path + '/cache')

# Remove the cache folder and all files
print(cache_path + ' folder has been removed.')
shutil.rmtree(cache_path)

# Create the cache folder again
print(cache_path + ' folder was created.')
os.mkdir(cache_path)

# Store the all pictures
pictures_list = []


def get_file_path_form_dir(path, store_list):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        temp = []
        if os.path.isdir(file_path):
            get_file_path_form_dir(file_path, temp)
            store_list.append(temp)
        elif re.match('^.*\.(jpg|gif|png|bmp)(?i)', file_path):
            store_list.append(file_path)


get_file_path_form_dir(data_path, pictures_list)


""""
pictures_list:
[
  [biben1.jpg, biden2.jpg],
  [obama1.jpg, obama2.jpg, obama3.jpg]
  [brice1.jpg]
]

"""

for picture_list in pictures_list:
    i = 0
    folder_name = os.path.dirname(picture_list[0]).split('/')[-1]
    for file_path in picture_list:
        image = load_image_file(file_path)

        # Get one picture's face locations
        locations = face_locations(
            image, number_of_times_to_upsample=0, model="cnn")
        i += 1
        for location in locations:
            top, right, bottom, left = location
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)

            # Save the picture inside face into other folder
            output_path = os.path.abspath(
                father_path + '/cache/' + folder_name + str(i) + '.jpg')

            # Save the face image to a new picture
            pil_image.save(output_path)
            print(output_path + ' was saved.')

""""
bricechou
  -- file_paths
      -- [
           [0 1.jpg]
           [1 2.jpg]
           [2 3.jpg]
         ]
  -- encondgs
     -- [
          [0 xxx]
          [1 xxx]
          [2 xxx]
        ]
"""
