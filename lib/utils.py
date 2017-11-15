import re
import sys
import scipy.misc
import heapq
import numpy as np
from models.model_handler import *

# We need to solve the Chinese language issues
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    import dlib
except Exception as e:
    error_info = 'Please install dlib tools first. Error: ' + str(e) + '\n'
    print('\033[0;31m%s\033[0m' % error_info)
    quit()

face_detector = dlib.get_frontal_face_detector()

complex_predictor_model = get_complex_predictor_model()
complex_predictor = dlib.shape_predictor(complex_predictor_model)

simple_predictor_model = get_simple_predictor_model()
simple_predictor = dlib.shape_predictor(simple_predictor_model)

cnn_detection_model = get_cnn_detector_model()
cnn_detector = dlib.cnn_face_detection_model_v1(cnn_detection_model)

dlib_model = get_dlib_model()
face_encoder = dlib.face_recognition_model_v1(dlib_model)


def _rect_to_css(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()


def _css_to_rect(css):
    return dlib.rectangle(css[3], css[0], css[1], css[2])


def _trim_css_to_bounds(css, image_shape):
    return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)


def _raw_face_locations(img, number_of_times_to_upsample=1, model='hog'):
    if model == 'cnn':
        return cnn_detector(img, number_of_times_to_upsample)
    else:
        return face_detector(img, number_of_times_to_upsample)


def face_distance(face_encodings, face_to_compare):
    if len(face_encodings) == 0:
        return np.empty((0))

    return np.linalg.norm(face_encodings - face_to_compare, axis=1)


def load_image_file(file, mode='RGB'):
    """
    To get an picture file's numpy array

    Args:
      file_path: picture file name and file path like (.jpg, .png, .jpeg etc)

    Returns:
      picture's numpy array
    """
    return scipy.misc.imread(file, mode=mode)


def face_locations(img, number_of_times_to_upsample=1, model='hog'):
    """
    To get an array of bounding boxes of human faces in a image

    Args:
      picture_numpy_array: picture file's numpy array.
      loop_times: higher numbers will find a smaller faces.
      handler_model: Which face detection model to use.
                ('hog' or 'cnn', 'hog' is less accurate but faster on CPUs.)

    Returns:
      A list of tuples of found face locations in css
        (top, right, bottom, left) order
    """

    if model == 'cnn':
        return [_trim_css_to_bounds(_rect_to_css(face.rect), img.shape) for face in _raw_face_locations(img, number_of_times_to_upsample, 'cnn')]
    else:
        return [_trim_css_to_bounds(_rect_to_css(face), img.shape) for face in _raw_face_locations(img, number_of_times_to_upsample, model)]


def _raw_face_landmarks(face_image, face_locations=None, model='small'):
    if face_locations is None:
        face_locations = _raw_face_locations(face_image)
    else:
        face_locations = [_css_to_rect(face_location) for face_location in face_locations]

    pose_predictor = simple_predictor

    if model == 'large':
        pose_predictor = complex_predictor

    return [
        pose_predictor(face_image, face_location)
        for face_location in
        face_locations]


def face_encodings(face_image, known_face_locations=None,
                   num_jitters=1, training_model='small'):
    raw_landmarks = _raw_face_landmarks(
        face_image, known_face_locations, training_model)

    return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters)) for raw_landmark_set in raw_landmarks]


def compare_faces(known_face_encodings, known_face_names,
                  face_encoding_to_check, tolerance=0.6):
    face_name = ''

    match_list = []

    print(face_distance(known_face_encodings, face_encoding_to_check))

    match_list = list(face_distance(known_face_encodings,
                                    face_encoding_to_check))

    get_match_index = map(match_list.index, heapq.nsmallest(1, match_list))

    for index in list(get_match_index):
        print('\nCurrent min distance value is \033[0;32m' +
              str(match_list[index]) + '\033[0m and who name is \033[0;32m' +
              str(known_face_names[index]) + '\033[0m.\n')
        if match_list[index] <= tolerance:
            face_name = re.match('\D*', known_face_names[index]).group()
            print('\033[0;32m' + face_name +
                  '\033[0m was found in distance_array\033[0;32m[' +
                  str(index) + ']\033[0m and distance value is \033[0;32m' +
                  str(match_list[index]) + '\033[0m.\n')

    return face_name
