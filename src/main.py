from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from src.SQLManagement import SQLManagement, searchColumns
from src.Img2VecResnet18 import Img2VecResnet18

import os.path

# create Flask app
PATH_ROOT = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))
PATH_STATIC = os.path.join(PATH_ROOT, "static/")
PATH_IMAGES = os.path.join(PATH_ROOT, "images/")
PATH_IMAGES_CNN = os.path.join(PATH_IMAGES, "cnn")
PATH_IMAGES_RAW = os.path.join(PATH_IMAGES, "raw")

app = Flask(__name__, static_folder=PATH_STATIC)
CORS(app)

# generate sql management
sqlManagement = SQLManagement(reload=True)

# setup convolutional neural network
recognizer: Img2VecResnet18 = Img2VecResnet18(reload=True)
recognizer.updateSimilarityMatrix(k=10)

@app.route('/')
def index():
    """
    Returns index.html when Flask is queried at /
    
    Returns:
        HTML file - dist/index.html
    """

    print("called for index")
    return app.send_static_file("dist/index.html")


@app.route("/api/search/<string:query>")
def search(query: str):
    results = sqlManagement.getRowsWithValue(value=query, columns=searchColumns)
    return jsonify(results), 201 


@app.route("/api/similar_to/<string:source>/", defaults={'accuracy': 70, 'max': 10})
@app.route("/api/similar_to/<string:source>/<int:accuracy>/<int:max>")
def find_similar_to(source: str, accuracy: int, max: int):
    """Returns similar images to source in reponse to api GET request.
    Access using /api/similar_to/<string:source>/<int:accuracy>/<int:max>

    Args:
        source (str): SQL index or filename of ImageEntity
        accuracy (int): Only return recommendations with greater certainty than accuracy. Ranges from 0 to 100.
        max (int): Maximum number of ImageEntity to return

    Returns:
        JSON - {List[Dict[str,str]]} - list of sql rows as json.

    """

    print("Creating Recognition for " + source)
    
    # recognizer.updateSimilarityMatrix(k=max)

    if source.isdigit():
        filename = sqlManagement.getRowsWithValue(value=source, columns=["id"], maxRows=1)[0]["filename"]
    else:
        filename = sqlManagement.getRowsWithValue(value=source,  columns=["filename"], maxRows=1)[0]["filename"]

    if not filename:
        return source + " Not Found", 401

    simImages, simValues = recognizer.getSimilarImages(filename)

    similarImages = []
    for i in range(len(simImages)):
        if simValues[i] >= accuracy / 100:
            for row in sqlManagement.getRowsWithValue(value=simImages[i], columns=["filename"]):
                similarImages.append(row)

    return jsonify(similarImages), 201


@app.route('/api/search/') # If no search term, serve all images 
@app.route('/api/images')
def get_images():
    """Returns all images in database.
    Access using /api/images

    Returns:
        List of dictionaries as JSON.

    """
    print("Getting images")

    return jsonify(sqlManagement.getAllRows()), 201


@app.route('/<path>/')
def redirect(path):
    '''Redirects calls to dist folder'''
    print("Redirecting " + path)
    return app.send_static_file("dist/" + path)


@app.route('/images/<path:path>/')
def redirect_images(path):
    '''Redirects images from images folder'''
    print("Redirecting " + path)
    return send_from_directory(PATH_IMAGES_CNN, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)


"""
1. Tests
2. Doc
3. Cloud Provider
"""

# @app.route('/api/images', methods=['POST'])
# def add_image():

#     print("Received Post for new image")

#     if request.get_json() == None:
#         return "No JSON was received"

#     posted_image = ImageSchema(only=('filename', 'description')).load(request.get_json())
#     image = ImageEntity(**posted_image)
    
#     # Save to database
#     sqlManagement.addImageRecord(image)

#     # Create response to confirm POST
#     new_image = ImageSchema().dump(image)
#     return jsonify(new_image), 201