__author__ = 'Brice Chou'

from pkg_resources import resource_filename

def get_complex_predictor_model():
    return resource_filename(__name__, "face_landmarks_68.dat")

def get_simple_predictor_model():
    return resource_filename(__name__, "face_landmarks_5.dat")

def get_dlib_model():
    return resource_filename(__name__, "dlib_model.dat")

def get_cnn_detector_model():
    return resource_filename(__name__, "face_detector.dat")
