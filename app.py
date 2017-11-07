import sys
import os
from lib.utils import face_locations, compare_faces, face_encodings

try:
    import cv2
    import h5py
except Exception as e:
    error_info = 'Please install cv2/h5py tools first. Error: ' + str(e) + '\n'
    print('\033[0;31m%s\033[0m' % error_info)
    quit()

# We need to solve the Chinese language issues
reload(sys)
sys.setdefaultencoding('utf-8')

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

cache_file_path = os.path.abspath('cache/cache.hdf5')

filerd = h5py.File(cache_file_path, 'r')

# Initialize some variables
i = 1
# counts = 1
# tiemout = 1000

face_names = []

screen_locations = []
screen_encodings = []

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

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        screen_locations = face_locations(small_frame)
        screen_encodings = face_encodings(
            small_frame, screen_locations, 1, 'small')
        face_names = []

        # How manay faces in the screen
        detected_face_length = len(screen_encodings)
        print('We detected \033[0;32m' + str(detected_face_length) +
              '\033[0m faces in the screen.')

        if detected_face_length >= 1:
            for screen_encoding in screen_encodings:
                # Compare the locations and get the face's name
                name = compare_faces(training_eigenvalues,
                                     training_names, screen_encoding, 0.4035)
                face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(screen_locations, face_names):
        # We detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left - 60, bottom + 30),
                      (right + 60, bottom - 10), (0, 0, 255), cv2.FILLED)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left - 50, bottom + 20),
                    font, 1, (255, 255, 255), 1)

    # Display the resulting image
    cv2.namedWindow('T2M', cv2.WINDOW_GUI_EXPANDED)
    cv2.imshow('T2M', frame)

    # We could use timeout to make a scrrenshot
    # if 0 == counts%tiemout:
    #     cv2.imwrite('cache/' + str(i) + '.jpg', frame)
    # counts += 1

    key = cv2.waitKey(10)
    if key == ord('s'):
        cv2.imwrite('cache/' + str(i) + '.jpg', frame)
        i = i + 1
    elif key == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
