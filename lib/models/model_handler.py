__author__ = 'Brice Chou'

from pkg_resources import resource_filename


def get_complex_predictor_model():
    """ predictor 68 face landmarks
    """

    return resource_filename(__name__, 'face_landmarks_68.dat')


def get_simple_predictor_model():
    """ predictor 5 face landmarks
    """

    return resource_filename(__name__, 'face_landmarks_5.dat')


def get_dlib_model():
    """ dlib face recognition resnet model_v1
    """

    return resource_filename(__name__, 'dlib_model.dat')


def get_cnn_detector_model():
    """ mmod human face detector
    """

    return resource_filename(__name__, 'face_detector.dat')
