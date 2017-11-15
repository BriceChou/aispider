import os
import re
import sys
from PIL import Image

# Extend on our system's path and can load the other folder's file
sys.path.append('..')
from lib.utils import face_locations, load_image_file


def delete_files(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.jpg'):
                os.remove(os.path.join(root, name))
                print(os.path.join(root, name) + ' was removed.')


def get_file_path_form_dir(path, store_list):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        temp = []
        if os.path.isdir(file_path):
            get_file_path_form_dir(file_path, temp)
            store_list.append(temp)
        elif re.match('^.*\.(jpg|gif|png|bmp)(?i)', file_path):
            store_list.append(file_path)


# Get current file's path
pwd = os.getcwd()

# Get project's path
project_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + '.')

# Get data's and cache's path
data_path = os.path.abspath(project_path + '/data')
cache_path = os.path.abspath(project_path + '/cache')

# Store the all pictures
pictures_list = []

# delete all jpg type files
delete_files(cache_path)

get_file_path_form_dir(data_path, pictures_list)

for picture_list in pictures_list:
    i = 0
    folder_name = os.path.dirname(picture_list[0]).split('/')[-1]
    for file_path in picture_list:
        print(file_path)
        image = load_image_file(file_path)

        # Get one picture's face locations
        locations = face_locations(image, 1, 'hog')
        i += 1
        for location in locations:
            top, right, bottom, left = location
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)

            # Save the picture inside face into other folder
            output_path = os.path.abspath(cache_path + '/' +
                                          folder_name + str(i) + '.jpg')

            # Save the face image to a new picture
            pil_image.save(output_path)
            print(output_path + ' was saved.')
