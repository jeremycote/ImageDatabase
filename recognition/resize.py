from torchvision import transforms

import os
from PIL import Image

def transformImages(inputDir, inputDirCNN):
    transformationForCNNInput = transforms.Compose([transforms.Resize((224,224))])
    
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
    path = os.path.join(root, inputDir)
    out = os.path.join(root, inputDirCNN)

    for imageName in os.listdir(path):
        I = Image.open(os.path.join(path, imageName))
        newI = transformationForCNNInput(I)

        if "exif" in I.info:
            exif = I.info['exif']
            newI.save(os.path.join(out, imageName), exif=exif)
        else:
            newI.save(os.path.join(out, imageName))

if __name__ == '__main__':
    inputDir = "images/raw"
    outputDir = "images/cnn"

    transformImages(inputDir, outputDir)