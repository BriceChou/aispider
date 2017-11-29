import re
import scipy.misc
import heapq
import numpy as np
from collections import Counter
from models.model_handler import *

try:
    import dlib
except Exception as e:
    error_info = 'Please install dlib tools first. Error: {}.\n'.format(e)
    print('\033[0;31m%s\033[0m' % error_info)
    quit()

_enable_debug = False

# Load all detector models
face_detector = dlib.get_frontal_face_detector()
cnn_detection_model = get_cnn_detector_model()
cnn_detector = dlib.cnn_face_detection_model_v1(cnn_detection_model)

# Load all predictor models
complex_predictor_model = get_complex_predictor_model()
complex_predictor = dlib.shape_predictor(complex_predictor_model)
simple_predictor_model = get_simple_predictor_model()
simple_predictor = dlib.shape_predictor(simple_predictor_model)

# Load dlib image encoder models
dlib_model = get_dlib_model()
face_encoder = dlib.face_recognition_model_v1(dlib_model)


def _debug(str):
    if _enable_debug: print('%s\n' % str)

def _rect_to_css(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()


def _css_to_rect(css):
    return dlib.rectangle(css[3], css[0], css[1], css[2])


def _trim_css_to_bounds(css, image_shape):
    return (max(css[0], 0), min(css[1], image_shape[1]),
            min(css[2], image_shape[0]),
            max(css[3], 0))


def _raw_face_landmarks(face_image, face_locations=None, model='small'):
    if face_locations is None:
        face_locations = _raw_face_locations(face_image)
    else:
        face_locations = [_css_to_rect(face_location)
                          for face_location in face_locations]

    pose_predictor = simple_predictor

    if model == 'large':
        pose_predictor = complex_predictor

    return [pose_predictor(face_image, face_location)
            for face_location in
            face_locations]


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

    _face_locations_mat = _raw_face_locations(img,
                                              number_of_times_to_upsample,
                                              model)
    if model == 'cnn':
        return [_trim_css_to_bounds(_rect_to_css(face.rect), img.shape)
                for face in _face_locations_mat]
    else:
        return [_trim_css_to_bounds(_rect_to_css(face), img.shape)
                for face in _face_locations_mat]


def face_encodings(face_image, known_face_locations=None,
                   num_jitters=1, training_model='small'):
    _raw_landmarks = _raw_face_landmarks(
        face_image, known_face_locations, training_model)

    return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters))
            for raw_landmark_set in _raw_landmarks]


def compare_faces(known_face_encodings, known_face_names,
                  face_encoding_to_check, tolerance=0.6):
    """ Compare the face in the video

    Args:
        known_face_encodings: Training face encodings mat
        known_face_names: Training face name list
        face_encoding_to_check:
        tolerance:

    Returns:
        predict this possible face name
    """

    face_name = ''
    match_list = []
    face_list = []

    match_list = list(face_distance(known_face_encodings,
                                    face_encoding_to_check))

    get_match_index = map(match_list.index, heapq.nsmallest(10, match_list))
    min_match_index = get_match_index[0]

    for index in get_match_index:
        match_info = ('Current min distance value is \033[0;32m{}\033[0m'
                      ' and who name is \033[0;32m{}\033[0m.')
        _debug(match_info.format(match_list[index], known_face_names[index]))

        if match_list[index] <= tolerance:
            face_name = re.match('\D*', known_face_names[index]).group()
            face_list.append(face_name)
            name_info = ('\033[0;32m{}\033[0m was found in distance_array\033[0;32m[{}]\033[0m'
                         ' and distance value is \033[0;32m{}\033[0m.')
            _debug(name_info.format(face_name, index, match_list[index]))

    # If we only can get one name from our database,
    # we should use the default one to display.
    if face_list:
        counter = Counter(face_list).most_common(1)
        most_possible_name = counter[0][0]
        name_frequency_number = counter[0][1]

        # If we get different name from our database,
        # we should also use the default one to display.
        if name_frequency_number == 1:
            face_name = re.match('\D*', known_face_names[min_match_index]).group()
        elif most_possible_name: face_name = most_possible_name
    else: face_name = re.match('\D*', known_face_names[min_match_index]).group()

    return face_name
