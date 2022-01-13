from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import json
from numpy import e, integer

from sqlalchemy import sql

from entities.ImageEntity import ImageEntity, ImageSchema
from entities.SQLManagement import SQLManagement

from recognition.recognition import Recognition

# create Flask app
app = Flask(__name__)
CORS(app)
app.config["IMAGES"] = "images/raw"


# generate sql management
sqlManagement = SQLManagement(reload=True)

# setup convolutional neural network
recognizer: Recognition = Recognition(True)
recognizer.updateSimilarityMatrix(k=10)

@app.route('/')
def index():
    print("called for index")
    return app.send_static_file("dist/index.html")

@app.route("/api/similar_to/<string:source>/<int:accuracy>/<int:max>")
def find_similar_to(source: str, accuracy: int, max: int):
    '''Find similar images to source.'''

    print("Creating Recognition for " + source)
    
    # recognizer.updateSimilarityMatrix(k=max)

    filename = ""
    if source.isdigit():
        filename = sqlManagement.getElementWithId(int(source)).filename
    else:
        elements = sqlManagement.getElementsWithFilename(source)
        if elements:
            filename = elements[0].filename
        else:
            return source + "Not found", 401

    simImages, simValues = recognizer.getSimilarImages(filename)

    imageEntities: ImageEntity = []
    for i in range(len(simImages)):
        if simValues[i] >= accuracy / 100:
            for entity in sqlManagement.getImageEntitiesWithFilename(simImages[i]):
                imageEntities.append(entity)

    return jsonify(imageEntities), 201
    # return send_from_directory(app.config["IMAGES"], simImages[0], as_attachment=False)

@app.route('/api/images')
def get_images():
    '''Get Images from SQL database'''
    print("Getting images")

    # fetch from database
    return jsonify(sqlManagement.getAllImageRecords()), 201

@app.route('/api/images', methods=['POST'])
def add_image():

    print("Received Post for new image")

    if request.get_json() == None:
        return "No JSON was received"

    posted_image = ImageSchema(only=('filename', 'description')).load(request.get_json())
    image = ImageEntity(**posted_image)
    
    # Save to database
    sqlManagement.addImageRecord(image)

    # Create response to confirm POST
    new_image = ImageSchema().dump(image)
    return jsonify(new_image), 201

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