import os
import re
import sys
import h5py
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

cache_file_path = os.path.abspath(cache_path + '/cache.hdf5')

filewt = h5py.File(cache_file_path, 'w')

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
    # i = 0
    # TODO: We should save the picture's path and file into database
    folder_name = os.path.dirname(picture_list[0]).split('/')[-1]
    # group = filewt.create_group(folder_name + '/file_paths')
    for file_path in picture_list:
        image = load_image_file(file_path)

        # Get one picture's face locations
        locations = face_locations(
            image, number_of_times_to_upsample=0, model="hog")
        # i += 1
        temp_list = []
        for location in locations:
            top, right, bottom, left = location
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)

            # TODO: We should support the more images training
            # output_path = os.path.abspath(
            #     father_path + '/cache/' + folder_name + str(i) + '.jpg')

            # Save the picture inside face into other folder
            output_path = os.path.abspath(
                father_path + '/cache/' + folder_name + '.jpg')
            temp_list.append(output_path)

            # Save the face image to a new picture
            pil_image.save(output_path)

        # Print new image's path
        for file_path in temp_list:
            print(file_path + ' was saved.')

        # Save the file's path into group
        # group[folder_name + '/file_paths'].create_dataset()

# filewt.close()

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
