from entities.Entity import Session, engine, Base
from entities.ImageEntity import ImageEntity

# generate database schema
Base.metadata.create_all(engine)

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