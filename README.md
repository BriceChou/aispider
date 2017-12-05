## AI Spider for face recognition

### Dependencies

You should install below as tools before you wanna start.

* `python` == `2.7.x`
* `dlib` >= `19.7`
* `opencv`
* `numpy`
* `scipy` >= `0.17.0`
* `h5py`

### How to use

you can run below as commands to start our project.

````python

    # To catch your face from Camera and save your image file into data/{you name} folder
    python app.py catch Brice.Chou

    # To auto roate the data folder image and auto {amount} times (current default times is 3)
    python app.py roate 3

    # To save your data folder's image training eigenvalue
    # into database/training_encodings.hdf5
    python app.py save

    # To run our face recognition program
    python app.py run

    # To detect all data folder image file's face and
    # save the new face image file into cache folder
    python app.py detect

    # To move your data folder's image file into cache folder and
    # name it with folder name
    python app.py move

````

## Aispider project's folder structure

### `data`

  First, we should create a folder and name it with the image's owner name.
  For example, we have a image file named `Stephen111.jpg`. It should be a image for `Stephen Chow`. So we should name the folder with `Stephen.Chow`.

  ````
  ├── data
  │   ├──Stephen.Chow
  │   │   ├── x1.png
  │   │   ├── Stephen.png
  │   │   ├── ob81.jpg
  │   │   ├── IMG_2226.JPG
  │   │   ├── Stephen111.jpg
  ````

  Then, you could put any image file with any name into this folder. Be noticed, you should only put the same person image into the same folder. Don't push any other person into a same folder. If you do, don't worry about it. We can auto split this image face into new face image file.

  Finally, you can name the main image file with `1.jpg`, `11.jpg`, `111.jpg` (current default value, because we can quickly name the image file). Or you can change the source code with other name as you wish.

### `cache`

  We would save some temporary files or datasets.
  For example, we would save the new face image from origin image in this folder. And we also create a new folder to save this new face image. More details you can see the `detect_face_from_picture.py` file's source code.

### `database`

  `TODO`: We should save every person into a individual hdf5 file.
  Currently, we save all training image's encodings into the same file which named "training_encodings.hdf5"

### `lib`
  our utils files or other 3rd-party python scripts
  * `files.py`: Mainly focus on handle the folder and image file. Such as remove the image file, create a new folder or file, get the iamge file from folder.
  * `utils.py`: Mainly focus on handle face recognition.
  * `databse.py`: Mainly focus on handle dataset saving and creating.
  * `models`: some predictor and detector models and datasets.

### `training`
  handle the pictures or videos training.
  * `catch_image_from_camera.py`: Capturing the training images from Camera. It will save the image file into `cache` folder.
  * `detect_face_from_picture.py`: It will find the face from image file and create a new face image file. It will auto save the new face image into `cache` folder.
  * `move_picture_into_cache.py`: It will auto move all 'data' folder image into `cache` foler with new name.
  * `save_training_encoding.py`: It will auto save the image's encodings dataset into 'database/training_encodings.hdf5' file.
  * `auto_rotate_image.py`: This tools will help you to auto rotate the image. If you have less image file or training file, you can use this script to generate more image files.

### `unknown`
  Mainly save the unknown person image. If someone is not in the training database, we would save the screenshot into this folder.

### `app.py`
 our application main entrance. We would also save the unknown person image into `unknown` folder.

---
#### Thanks,
````
Name: Mingliang ZHOU
Skype: bricechou
Nick-Name: Brice Chou
E-mail: bricechou@gmail.com
````
