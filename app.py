import sys
import cv2
import h5py
import os
from lib.utils import face_locations, compare_faces, face_encodings

# We need to solve the Chinese language issues
reload(sys)
sys.setdefaultencoding('utf-8')

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

cache_file_path = os.path.abspath('cache/cache.hdf5')

filerd = h5py.File(cache_file_path, 'r')

# Initialize some variables
face_locs = []
face_ens = []
face_names = []
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
        face_locs = face_locations(small_frame)
        face_ens = face_encodings(
            small_frame, face_locs, 1, training_model='small')
        face_names = []

        # How manay faces in the screen
        detected_face_length = len(face_ens)
        print('We detected \033[0;32m' + str(detected_face_length) +
              '\033[0m faces in the screen.')

        if detected_face_length >= 1:
            for face_encoding in face_ens:
                # See if the face is a match for the known face(s)
                name = compare_faces(training_eigenvalues,
                                     training_names, face_encoding, 0.4035)
                face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locs, face_names):
        # Scale back up face locations
        #   since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left - 50, bottom + 30),
                      (right + 50, bottom - 10), (0, 0, 255), cv2.FILLED)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left - 30, bottom + 20),
                    font, 1, (255, 255, 255), 1)

    # Display the resulting image
    cv2.namedWindow('T2M', cv2.WINDOW_GUI_EXPANDED)
    cv2.imshow('T2M', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
