__author__ = 'Brice Chou'

import os
import sys
import h5py
from PIL import Image

# Extend on our system's path and can load the other folder's file
sys.path.append('..')
import lib

# Use the utf-8 coded format
reload(sys)
sys.setdefaultencoding('utf-8')


def save(project_path=''):
    # Get data folder path
    data_folder_path = os.path.abspath(project_path + 'data')
    cache_folder_path = os.path.abspath(project_path + 'cache')
    database_file_path = os.path.abspath(project_path +
                                         'database/training_encodings.hdf5')

    fid = h5py.File(database_file_path, 'a')

    # Store the all pictures
    main_image_list = []
    other_image_list = []

    # Store the main image encodings and names
    training_names = []
    training_eigenvalues = []

    # Image encodings mode
    encodings_mode = 'large'

    # For more complex mode you can set it to 'cnn'
    detector_mode = 'cnn'

    # How many times to upsample the image file
    detector_times = 1

    # How much distance between current faces to known faces
    min_tolerance = 0.5

    lib.get_main_and_other_images(data_folder_path, main_image_list,
                                  other_image_list)
    start_index = 0

    # Save the main image encodings
    for image_path in main_image_list:
        main_folder_name = lib.get_folder_name_by_file(image_path)
        start_index += 1
        try:
            main_image = lib.load_image_file(image_path)
            main_locations = lib.face_locations(main_image, detector_times,
                                                detector_mode)

            locations_length = len(main_locations)
            if locations_length > 1:
                print('There is more than one face in %s' % image_path)
            else:
                main_label = '{}{}'.format(main_folder_name, start_index)
                main_image_ecoding = lib.face_encodings(main_image, None,
                                                        2, encodings_mode)[0]
                lib.save_data(fid, main_label, main_image_ecoding)
        except Exception as e:
            error_info = '{}: \033[0;31m{}\033[0m.'.format(main_folder_name, e)
            print('Save main image %s' % error_info)
            continue

    # Get the main image encodings data
    for key in fid.keys():
        training_eigenvalues.append(fid[key].value)
        training_names.append(fid[key].name.split('/')[-1])

    # Save the other image encodings data
    for file_path in other_image_list:
        folder_name = lib.get_folder_name(file_path)
        image = lib.load_image_file(file_path)
        i = lib.get_max_index_from_name_list(folder_name, training_names)
        try:
            locations = lib.face_locations(image, detector_times,
                                           detector_mode)
            locations_length = len(locations)

            if locations_length > 1:
                print('There is more than one face in %s' % file_path)

                # Create a new folder to save the new image
                new_folder_path = os.path.join(cache_folder_path, folder_name)
                lib.create_folder_with_path(new_folder_path)
                j = lib.get_file_max_number(new_folder_path)

                file_type = lib.get_file_type(file_path)

                for location in locations:
                    top, right, bottom, left = location
                    right += 10
                    bottom += 10

                    face_image = image[top:bottom, left:right]
                    pil_image = Image.fromarray(face_image)

                    # Save the picture inside face into other folder
                    output_path = '{}/{}{}.{}'.format(new_folder_path,
                                                      folder_name, j,
                                                      file_type)

                    # Save the face image to a new picture
                    pil_image.save(output_path)
                    j += 1
                    print('Training image: \033[0;32m%s\033[0m'
                          ' was saved.' % output_path)
            else:
                encodings = lib.face_encodings(image, None,
                                               2, encodings_mode)
                for encoding in encodings:
                    i += 1
                    file_label = '{}{}'.format(folder_name, i)
                    name = lib.compare_faces(training_eigenvalues,
                                             training_names,
                                             encoding, min_tolerance)

                    print('folder name is \033[0;32m%s\033[0m,'
                          ' current name is \033[0;32m%s\033[0m' %
                          (folder_name, name))
                    if folder_name == name:
                        training_names.append(file_label)
                        # Save the image locations into database
                        lib.save_data(fid, file_label, encoding)
        except Exception as e:
            error_info = '{}: \033[0;31m{}\033[0m.'.format(file_path, e)
            print('Save other image %s' % error_info)
            continue

    lib.print_all_data_name(fid)

    fid.close()


if __name__ == '__main__':
    save('../')
