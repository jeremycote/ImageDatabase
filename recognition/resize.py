from torchvision import transforms

import os
from PIL import Image

def transformImages(inputDir, inputDirCNN):
    transformationForCNNInput = transforms.Compose([transforms.Resize((224,224))])
    for imageName in os.listdir(inputDir):
        I = Image.open(os.path.join(inputDir, imageName))
        newI = transformationForCNNInput(I)

        if "exif" in I.info:
            exif = I.info['exif']
            newI.save(os.path.join(inputDirCNN, imageName), exif=exif)
        else:
            newI.save(os.path.join(inputDirCNN, imageName))

if __name__ == '__main__':
    inputDir = "images/raw"
    outputDir = "images/cnn"

    transformImages(inputDir, outputDir)