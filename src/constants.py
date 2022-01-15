import os.path

#: Absolute path to project root directory. Calculated automatically.
PATH_ROOT = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))

#: Absolute path to project static directory. Calculated automatically.
PATH_STATIC = os.path.join(PATH_ROOT, "static/")

#: Absolute path to project images directory. Calculated automatically.
PATH_IMAGES = os.path.join(PATH_ROOT, "images/")

#: Absolute path to project images/cnn directory. Calculated automatically.
PATH_IMAGES_CNN = os.path.join(PATH_IMAGES, "cnn")

#: Absolute path to project images/raw directory. Calculated automatically.
PATH_IMAGES_RAW = os.path.join(PATH_IMAGES, "raw")

#: Absolute path to project database file. Calculated automatically.
PATH_DB = os.path.join(PATH_ROOT, "src/database.db")