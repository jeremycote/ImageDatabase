from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import json
from numpy import e, integer

from sqlalchemy import sql

from database.SQLManagement import SQLManagement, exifAttributes

from recognition.recognition import Recognition

# create Flask app
app = Flask(__name__)
CORS(app)

# generate sql management
sqlManagement = SQLManagement(reload=False)

# setup convolutional neural network
recognizer: Recognition = Recognition(reload=False)
recognizer.updateSimilarityMatrix(k=10)

# search
searchColumns = ["filename"] + [attribute[0] for attribute in exifAttributes]

@app.route('/')
def index():
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
        list of ImageEntity as json.

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

@app.route('/api/search/')
@app.route('/api/images')
def get_images():
    '''Get Images from SQL database'''
    print("Getting images")

    # fetch from database
    images = jsonify(sqlManagement.getAllImageRecords())
    print(sqlManagement.getAllImageRecords()[1])
    return images, 201

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

@app.route('/<path>/')
def redirect(path):
    '''Redirects calls to dist folder'''
    print("Redirecting " + path)
    return app.send_static_file("dist/" + path)

@app.route('/images/<path:path>/')
def redirect_images(path):
    '''Redirects images from images folder'''
    print("Redirecting " + path)
    return send_from_directory("images/cnn", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


"""
1. Tests
2. Doc
3. Cloud Provider
"""