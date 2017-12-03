import os
import sys
import h5py

# Use the utf-8 coded format
reload(sys)
sys.setdefaultencoding('utf-8')

# Extend on our system's path and can load the other folder's file
sys.path.append('..')
import lib

# Get data folder path
data_folder_path = os.path.abspath('../data')
database_file_path = os.path.abspath('../database/training_encodings.hdf5')
fid = h5py.File(database_file_path, 'a')

# Store the all pictures
main_image_list = []
other_image_list = []
training_eigenvalues = []

# Image encodings mode
encodings_mode = 'small'

# For more complex mode you can set it to 'cnn'
detector_mode = 'hog'

# How many times to upsample the image looking for faces
detect_times = 3

lib.get_main_and_other_images(data_folder_path, main_image_list,
                              other_image_list)

# Save the main image encodings
for image_path in main_image_list:
    file_name = lib.get_file_name(image_path)
    main_folder_name = os.path.dirname(image_path).split('/')[-1]
    try:
        main_image = lib.load_image_file(image_path)
        main_locations = lib.face_locations(main_image, detect_times,
                                            detector_mode)
        main_image_ecoding = lib.face_encodings(main_image, main_locations,
                                                3, encodings_mode)[0]
        lib.save_data(fid, main_folder_name, main_image_ecoding)
    except Exception as e:
        error_info = 'Save {} Error: {}.\n'.format(main_folder_name, e)
        print('\033[0;31m%s\033[0m' % error_info)
        continue

# Get the main image encodings data
for key in fid.keys():
    training_eigenvalues.append(fid[key].value)

# Save the other image encodings data
for file_path in other_image_list:
    folder_name = os.path.dirname(file_path).split('/')[-1]
    i = lib.get_image_max_index(fid, folder_name)
    image = lib.load_image_file(file_path)
    try:
        # Get one picture's face locations
        locations = lib.face_locations(image, detect_times,
                                       detector_mode)
        encodings_mat = lib.face_encodings(image, locations,
                                           3, encodings_mode)[0]
        file_label = '{}{}'.format(folder_name, i)
        file_path_label = '%s_path' % file_label
        tolerance = lib.face_distance(training_eigenvalues,
                                      encodings_mat)
        if tolerance <= 0.6:
            # Save the image locations into database
            lib.save_data(fid, file_label, encodings_mat)
            lib.save_image_max_index(fid, folder_name, i)
    except Exception as e:
        error_info = 'Save {} Error: {}.\n'.format(file_path, e)
        print('\033[0;31m%s\033[0m' % error_info)
        continue

for key in fid.keys():
    print(key)

fid.close()
