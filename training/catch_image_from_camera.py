import os
import sys
import time

# Extend on our system's path and can load the other folder's file
sys.path.append('..')
from lib.utils import face_locations, face_encodings, get_file_max_number

try:
    import cv2
except Exception as e:
    error_info = 'Please install cv2/h5py tools first. Error: ' + str(e) + '\n'
    print('\033[0;31m%s\033[0m' % error_info)
    quit()

# We need to solve the Chinese language issues
reload(sys)
sys.setdefaultencoding('utf-8')

# Get current file's path
pwd = os.getcwd()

# Get project's path
project_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + '.')

# Get data's and cache's path
cache_path = os.path.abspath(project_path + '/cache')

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
i = get_file_max_number(cache_path)

screen_locations = []
screen_encodings = []

process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        screen_locations = face_locations(small_frame)
        screen_encodings = face_encodings(
            small_frame, screen_locations, 1, 'small')

        # How manay faces in the screen
        detected_face_length = len(screen_encodings)
        if detected_face_length >= 1:
            cv2.imwrite(cache_path + '/' + str(i) + '.jpg', frame)
            i += 1

    process_this_frame = not process_this_frame

    # Display the resulting image
    cv2.namedWindow('T2M', cv2.WINDOW_GUI_EXPANDED)
    cv2.imshow('T2M', frame)

    time.sleep(0.1)

    if cv2.waitKey(10) == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
