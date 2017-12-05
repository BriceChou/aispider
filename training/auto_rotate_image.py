__author__ = 'Brice Chou'

import os
import sys
import cv2
import math
import random

# Extend on our system's path and can load the other folder's file
sys.path.append('..')
import lib

# Use the utf-8 coded format
reload(sys)
sys.setdefaultencoding('utf-8')


def _create_new_image_with_degree(input_file_path, degree, output_path):
    image = cv2.imread(input_file_path)
    h, w = image.shape[:2]

    # calculate the rotated image new height
    n_h = int(w * math.fabs(math.sin(math.radians(degree))) +
              h * math.fabs(math.cos(math.radians(degree))))

    # calculate the rotated image new weight
    n_w = int(h * math.fabs(math.sin(math.radians(degree))) +
              w * math.fabs(math.cos(math.radians(degree))))

    rotation_mat = cv2.getRotationMatrix2D(
        (w / 2, h / 2), degree, 1)

    rotation_mat[0, 2] += (n_w - w) / 2
    rotation_mat[1, 2] += (n_h - h) / 2

    new_rotated_image = cv2.warpAffine(
        image, rotation_mat, (n_w, n_h), borderValue=(255, 255, 255))

    # Save the rotated image to a new picture
    cv2.imwrite(output_path, new_rotated_image)
    print('new rotated image: \033[0;32m%s\033[0m.' % output_path)


def rotate(project_path=''):
    # Get data folder's path
    data_folder_path = os.path.abspath(project_path + 'data')

    # Store the all image file's path
    image_file_list = []

    # How many rotated image you wish
    amount = 3

    lib.get_image_path_from_folder_group_by(data_folder_path,
                                            image_file_list, False)

    for image_list in image_file_list:
        folder_path = os.path.dirname(image_list[0])
        folder_name = lib.get_folder_name_by_folder(folder_path)
        i = lib.get_file_max_number(folder_path, image_list)

        for file_path in image_list:
            i += 1
            file_type = lib.get_file_type(file_path)
            # Save the picture inside face into other folder
            output_path = '{}/{}{}.{}'.format(folder_path, folder_name,
                                              i, file_type)
            for degree in random.sample([x for x in range(-180, 180)], amount):
                _create_new_image_with_degree(file_path, degree, output_path)


if __name__ == '__main__':
    rotate('../')
