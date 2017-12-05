__author__ = 'Brice Chou'

import os
import lib
import sys
import time
import getopt
import training

try:
    import cv2
    import h5py
except Exception as e:
    error_info = 'Please install h5py/cv2 tools first. Error: {}.\n'.format(e)
    print('\033[0;31m%s\033[0m' % error_info)
    quit()


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def run():
    # Set the window name
    window_name = __author__

    # Get a reference to webcam #-1 (the last one)
    video_capture = cv2.VideoCapture(-1)

    # Initialize some variables
    unknown_folder_path = os.path.abspath('unknown')
    i = lib.get_file_max_number(unknown_folder_path)
    filerd = h5py.File('./database/training_encodings.hdf5', 'r')

    # Image encodings mode
    encodings_mode = 'hog'

    # Temp to save predict result name
    face_names = []

    # Save the screen locations and encodings to find a person
    screen_locations = []
    screen_encodings = []

    # Save the training data from database
    training_names = []
    training_eigenvalues = []

    process_this_frame = True

    for key in filerd.keys():
        training_names.append(filerd[key].name.split('/')[-1])
        training_eigenvalues.append(filerd[key].value)

    filerd.close()

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size
        # for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings
            # in the current frame of video
            screen_locations = lib.face_locations(small_frame)
            screen_encodings = lib.face_encodings(
                small_frame, screen_locations, 1, encodings_mode)
            face_names = []

            # How manay faces in the screen
            detected_face_length = len(screen_encodings)
            info = 'We detected \033[0;32m{}\033[0m faces in the screen.\n'
            print(info.format(detected_face_length))
            if detected_face_length >= 1:
                for screen_encoding in screen_encodings:
                    # Compare the locations and get the face's name
                    name = lib.compare_faces(training_eigenvalues,
                                             training_names,
                                             screen_encoding, 0.31)
                    face_names.append(name)

                    # Auto save the unknown images
                    if '' == name:
                        img_file_path = '{}/{}.jpg'.format(
                            unknown_folder_path, i)
                        cv2.imwrite(img_file_path, frame)
                        i += 1
                        time.sleep(0.15)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(screen_locations, face_names):
            # We detected in was scaled to 1/2 size
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            if '' != name:
                # Draw a label with a name below the face
                # # cv2.cv.CV_FILLED
                cv2.rectangle(frame, (left - 60, bottom + 30),
                              (right + 60, bottom - 10), (0, 0, 255),
                              cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left - 50, bottom + 20),
                            font, 1, (255, 255, 255), 1)

        # Display the resulting image
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        # cv2.cv.CV_WINDOW_FULLSCREEN
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1)
        if key == ord('s'):
            label = 'cache/{}.jpg'.format(i)
            cv2.imwrite(label, frame)
            i += 1
        elif key == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            argv_list = argv[1:]
            opts, args = getopt.getopt(argv_list, 'h', ['help'])
            arg = argv_list[0]
            if 'run' == arg:
                run()
            elif 'save' == arg:
                training.save()
            elif 'move' == arg:
                training.move()
            elif 'detect' == arg:
                training.detect()
            elif 'catch' == arg:
                if 2 == len(argv_list):
                    training.catch(argv_list[1])
                else:
                    training.catch()
            elif 'rotate' == arg:
                if 2 == len(argv_list):
                    training.rotate(amount=argv_list[1])
                else:
                    training.catch()
        except getopt.error, msg:
            raise Usage(msg)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, 'for help use --help'
        return 2


if __name__ == '__main__':
    sys.exit(main())
