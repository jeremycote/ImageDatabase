import os.path

PATH_ROOT = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))
PATH_STATIC = os.path.join(PATH_ROOT, "static/")
PATH_IMAGES = os.path.join(PATH_ROOT, "images/")
PATH_IMAGES_CNN = os.path.join(PATH_IMAGES, "cnn")
PATH_IMAGES_RAW = os.path.join(PATH_IMAGES, "raw")
PATH_DB = os.path.join(PATH_ROOT, "src/database.db")