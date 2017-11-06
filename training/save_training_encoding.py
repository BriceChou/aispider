import os
import re
import sys
import h5py

# Extend on our system's path and can load the other folder's file
sys.path.append('..')

# We need to solve the Chinese language issues
reload(sys)
sys.setdefaultencoding('utf-8')

from lib.utils import load_image_file, face_encodings, face_locations

# Get current file's path
pwd = os.getcwd()

# Get project's path
father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + '.')

# Get data's path
data_path = os.path.abspath(father_path + '/data')

cache_path = os.path.abspath(father_path + '/cache')

cache_file_path = os.path.abspath(cache_path + '/cache.hdf5')

print('\033[0;31m%s\033[0m' % cache_file_path + ' was removed.\n')
os.remove(cache_file_path)

fid = h5py.File(cache_file_path, 'w')

# Store the all pictures
pictures_list = []


def get_file_path_form_dir(path, store_list):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        temp = []
        if os.path.isdir(file_path):
            get_file_path_form_dir(file_path, temp)
            store_list.append(temp)
        # Load all files with .jpg, .png etc type
        # If we want to load file with .jpg or .JPG type file,
        # we could change the regular expression to
        # '^.*\.(jpg|gif|png|bmp)(?i)'
        elif re.match('^.*\.(jpg|gif|png|bmp)', file_path):
            store_list.append(file_path)


get_file_path_form_dir(data_path, pictures_list)


def get_file_name(file_path):
    print(file_path + ' encondings value was saved.')
    return os.path.splitext(file_path)[0].split('/')[-1]


for picture_list in pictures_list:
    i = 0
    folder_name = os.path.dirname(picture_list[0]).split('/')[-1]
    for file_path in picture_list:
        i += 1
        image = load_image_file(file_path)

        try:
            # Get one picture's face locations
            locations = face_locations(
                image, number_of_times_to_upsample=1, model="cnn")
            encodings_mat = face_encodings(image, locations, 3)[0]
            attr_label = folder_name + str(i)

            # Save the image locations into database
            fid.create_dataset(attr_label, data=encodings_mat)
            print('\033[0;32m%s\033[0m' % file_path + ' was saved.\n')

        except Exception as e:
            error_info = 'Save ' + file_path + ' Error: ' + str(e) + '\n'
            print('\033[0;31m%s\033[0m' % error_info)
            continue

fid.close()
