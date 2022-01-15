from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from src.SQLManagement import SQLManagement, searchColumns
from src.Img2VecResnet18 import Img2VecResnet18

from src.constants import PATH_STATIC, PATH_IMAGES_CNN, PATH_IMAGES_RAW

# create Flask app
app = Flask(__name__, static_folder=PATH_STATIC)
CORS(app)

# generate sql management
sqlManagement = SQLManagement(reload=True)

# setup convolutional neural network
recognizer: Img2VecResnet18 = Img2VecResnet18(reload=True)

@app.route('/')
def getIndex():
    """
    Returns index.html when Flask is queried at /
    
    Returns:
        HTML file - dist/index.html
    """

    print("called for index")
    return app.send_static_file("dist/index.html")


@app.route("/api/search/<string:query>")
def search(query: str, columns=searchColumns):
    """
    Returns SQL rows that contain query in passed columns
    Access using /api/search/<string:query>
    
    Args:
        query (str): value to search in database
        columns (List[str]): database columns to search inside. Defaults to searchColumns global variable.

    Returns:
        JSON - {List[Dict[str,str]]} - list of sql rows as json.
    """

    results = sqlManagement.getRowsWithValue(value=query, columns=columns)
    return jsonify(results), 201 


@app.route("/api/similar_to/<string:source>/", defaults={'accuracy': 70, 'max': 10})
@app.route("/api/similar_to/<string:source>/<int:accuracy>/<int:max>")
def find_similar_to(source: str, accuracy: int, max: int):
    """
    Returns similar images to source in reponse to api GET request.
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

    column = "filename"
    if source.isdigit():
        column = "id"
    
    results = sqlManagement.getRowsWithValue(value=source, columns=[column], maxRows=1)
    
    if len(results) == 0:
        return source + " is not in database", 401

    filename = results[0]["filename"]

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
    """
    Returns all rows in database.
    Access using /api/images

    Returns:
        JSON - {List[Dict[str,str]]} - list of sql rows as json.

    """
    print("Getting images")

    return jsonify(sqlManagement.getAllRows()), 201


@app.route('/<path>/')
def redirect(path):
    """
    Redirects calls to dist folder
    Args:
        path (str): path to file inside dist folder

    Returns:
        file at path
    """
    print("Redirecting " + path)
    return app.send_static_file("dist/" + path)


@app.route('/images/<string:quality>/<string:filename>/')
def redirect_images(quality: str, filename: str):
    """
    Returns Image with filename
    
    Args:
        quality (str): raw returns original, else return compressed
        filename (str): image filename

    Returns:
        Image file using send_from_directory
    """
    print("Redirecting " + filename)

    path: str
    if quality == "raw":
        path = PATH_IMAGES_RAW
    else:
        path = PATH_IMAGES_CNN
    
    return send_from_directory(path, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)

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