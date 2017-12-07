__author__ = 'Brice Chou'

import os
import cv2
import sys
import time

# Extend on our system's path and can load the other folder's file
sys.path.append('..')
import lib


def catch(image_owner_name='unknown', project_path=''):
    # Set the window name
    window_name = __author__

    # Get data folder's path
    data_folder_path = os.path.abspath(project_path + 'data')

    # If there is Camera accessory, we should use it first.
    video_capture = cv2.VideoCapture(-1)

    # you can set this value with your catch name
    new_folder_name = image_owner_name

    # Initialize the saved folder
    new_folder_path = '{}/{}'.format(data_folder_path,
                                     new_folder_name)
    lib.create_folder_with_path(new_folder_path)
    i = lib.get_file_max_number(new_folder_path)

    screen_locations = []
    screen_encodings = []

    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/2 size
        # for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Only process every other frame of video to save time
        if process_this_frame:

            # Find all the faces and face encodings
            # in the current frame of video
            screen_locations = lib.face_locations(small_frame)
            screen_encodings = lib.face_encodings(small_frame,
                                                  screen_locations,
                                                  1, 'small')

            # How manay faces in the screen
            detected_face_length = len(screen_encodings)
            if detected_face_length >= 1:
                new_image_label = '{}/{}.jpg'.format(new_folder_path, i)
                cv2.imwrite(new_image_label, frame)
                i += 1

        process_this_frame = not process_this_frame

        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, frame)

        time.sleep(0.1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    catch(project_path='../')
