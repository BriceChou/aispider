import os
import re
import sys
import h5py

# Extend on our system's path and can load the other folder's file
sys.path.append('..')

# We need to solve the Chinese language issues
reload(sys)
sys.setdefaultencoding('utf-8')

from lib.utils import load_image_file, face_encodings

# Get current file's path
pwd = os.getcwd()

# Get project's path
father_path = os.path.abspath(os.path.dirname(pwd) + os.path.sep + '.')

# Get data's path
cache_path = os.path.abspath(father_path + '/cache')

cache_file_path = os.path.abspath(cache_path + '/cache.hdf5')

filewt = h5py.File(cache_file_path, 'w')


def get_file_name(file_path):
    print(file_path + ' encondings saved.')
    return os.path.splitext(file_path)[0].split('/')[-1]


for file in os.listdir(cache_path):
    file_path = os.path.join(cache_path, file)
    if re.match('^.*\.(jpg|gif|png|bmp)(?i)', file_path):
        image = load_image_file(file_path)
        encodings_mat = face_encodings(image)[0]
        label = get_file_name(file_path)
        filewt.create_dataset(label, data=encodings_mat)

filewt.close()
