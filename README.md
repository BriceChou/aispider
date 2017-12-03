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

  Then, you could put any image file name into this folder. Be notice, it should only put the same person image. Don't push any other person into a same folder.

  Finally, you can name the main image file with `1.jpg` (current default value). Or you can change the source code with other name as you wish.

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
