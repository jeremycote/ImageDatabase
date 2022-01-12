from flask import Flask, jsonify, request, render_template

from entities.Entity import Session, engine, Base
from entities.ImageEntity import ImageEntity, ImageSchema

# create Flask app
app = Flask(__name__)

# generate database schema
Base.metadata.create_all(engine)

print("base gen")

@app.route('/')
def index():
    print("called for index")
    return app.send_static_file("dist/index.html")

@app.route('/<path>/')
def deb(path):
    print("Redirecting", path)
    return app.send_static_file("dist/" + path)

@app.route('/api/images')
def get_images():
    '''Get Images from SQL database'''
    print("Getting images")

    # fetch from database
    session = Session()
    image_objects = session.query(ImageEntity).all()

    # Convert SQL query to JSON-serializable objects
    schema = ImageSchema(many=True)
    images = schema.dump(image_objects)

    # serialize as JSON
    session.close()
    return jsonify(images)

@app.route('/images', methods=['POST'])
def add_image():

    print("Received Post for new image")

    if request.get_json() == None:
        return "None received"

    print(request.get_json())

    posted_image = ImageSchema(only=('filename', 'description')).load(request.get_json())
    print("Created posted_image")
    image = ImageEntity(**posted_image)
    print("Created image")
    session = Session()
    print("Created Session")
    session.add(image)
    print("Added image")
    session.commit()
    print("Commited")

    new_image = ImageSchema().dump(image)
    print("Created new_image")
    session.close()
    print("Closed session")
    return jsonify(new_image), 201

# start session
session = Session()

# check for existing data
images = session.query(ImageEntity).all()

if len(images) == 0:
    # Create and persiste example image entry
    image_cake = ImageEntity("Cake.jpg", "A Delicious piece of cake!")
    session.add(image_cake)
    session.commit()
    session.close()

    # Reload new images
    images = session.query(ImageEntity).all()

print("### Images in SQL: ")
for image in images:
    print(f"{image.id} {image.filename} - {image.description}")

if __name__ == "__main__":
    app.run(host="172.28.13.62", port=5000, debug=True)


"""
1. Tests
2. Doc
3. Cloud Provider
"""