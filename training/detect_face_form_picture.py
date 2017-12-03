import os
import sys
from PIL import Image

# Extend on our system's path and can load the other folder's file
sys.path.append('..')
import lib

# Use the utf-8 coded format
reload(sys)
sys.setdefaultencoding('utf-8')

# Get data's and cache's path
data_folder_path = os.path.abspath('../data')
cache_folder_path = os.path.abspath('../cache')

# For more complex mode you can set it to 'cnn'
detector_mode = 'hog'

# How many times to upsample the image looking for faces
detect_times = 3

# Store the all pictures path
pictures_list = []

lib.get_image_path_from_folder_group_by(data_folder_path, pictures_list, False)

for picture_list in pictures_list:
    folder_name = os.path.dirname(picture_list[0]).split('/')[-1]

    # Create a new folder to save the new image
    new_folder_path = os.path.join(cache_folder_path, folder_name)
    i = lib.get_file_max_number(new_folder_path)
    lib.create_new_folder(new_folder_path)

    for file_path in picture_list:
        image = lib.load_image_file(file_path)

        # Get one picture's face locations
        locations = lib.face_locations(image, detect_times,
                                       detector_mode)
        i += 1
        for location in locations:
            top, right, bottom, left = location
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)

            # Save the picture inside face into other folder
            output_path = ('{}/{}{}.jpg').format(new_folder_path,
                                                 folder_name, i)

            # Save the face image to a new picture
            pil_image.save(output_path)
            print('\033[0;32m%s\033[0m was saved.' % output_path)
