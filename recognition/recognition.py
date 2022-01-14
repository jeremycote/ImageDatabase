import os
import numpy as np
import pandas as pd
from PIL import Image
import torch
from torchvision import transforms
from tqdm import tqdm
from torchvision import models

from recognition.resize import transformImages

from numpy.testing import assert_almost_equal

from typing import List

class Recognition():
    def __init__(self, reload=False) -> None:
        self.img2vec = Img2VecResnet18()
        self.allVectors = {}

        root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
        self.inputDir = os.path.join(root, "images/cnn")

        if reload:
            transformImages("images/raw", "images/cnn")


    def updateSimilarityMatrix(self, k=5):
        
        self.k = k
    
        for image in tqdm(os.listdir(self.inputDir)):
            I = Image.open(os.path.join(self.inputDir, image))
            vec = self.img2vec.getVec(I)
            self.allVectors[image] = vec
            I.close()

        self.similarityMatrix = self.img2vec.getSimilarityMatrix(self.allVectors)

        self.similarNames = pd.DataFrame(index = self.similarityMatrix.index, columns = range(self.k))
        self.similarValues = pd.DataFrame(index = self.similarityMatrix.index, columns = range(self.k))

        for j in tqdm(range(self.similarityMatrix.shape[0])):
            kSimilar = self.similarityMatrix.iloc[j, :].sort_values(ascending = False).head(self.k)
            self.similarNames.iloc[j, :] = list(kSimilar.index)
            self.similarValues.iloc[j, :] = kSimilar.values

    def getSimilarImages(self, image):
        if image in set(self.similarNames.index):
            imgs = list(self.similarNames.loc[image, :])
            vals = list(self.similarValues.loc[image, :])
            
            if image in imgs:
                assert_almost_equal(max(vals), 1, decimal = 5)
                imgs.remove(image)
                vals.remove(max(vals))
        
            return imgs, vals
        else:
            print("'{}' Unknown image".format(image))

class Img2VecResnet18():
    def __init__(self):
        self.device = torch.device("cpu")
        self.numberFeatures = 512
        self.modelName = "resnet-18"
        self.model, self.featureLayer = self.getFeatureLayer()
        self.model = self.model.to(self.device)
        self.model.eval()
        self.toTensor = transforms.ToTensor()
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

    def getFeatureLayer(self):
        cnnModel = models.resnet18(pretrained=True)
        layer = cnnModel._modules.get('avgpool')
        self.layer_output_size = 512
        
        return cnnModel, layer
    
    def getVec(self, img):
        image = self.normalize(self.toTensor(img)).unsqueeze(0).to(self.device)
        embedding = torch.zeros(1, self.numberFeatures, 1, 1)
        def copyData(m, i, o): embedding.copy_(o.data)
        h = self.featureLayer.register_forward_hook(copyData)
        self.model(image)
        h.remove()
        return embedding.numpy()[0, :, 0, 0]

    def getSimilarityMatrix(self, vectors):
        v = np.array(list(vectors.values())).T
        sim = np.inner(v.T, v.T) / ((np.linalg.norm(v, axis=0).reshape(-1,1)) * ((np.linalg.norm(v, axis=0).reshape(-1,1)).T))
        keys = list(vectors.keys())
        matrix = pd.DataFrame(sim, columns = keys, index = keys)
        return matrix

if __name__ == '__main__':
    recognizer: Recognition = Recognition()

    inputImages = ["Cake.jpg"]
    for image in inputImages:
        simImages, simValues = recognizer.getSimilarImages(image)
        
        for i in range(len(simImages)):
            print(f"Image {simImages[i]} with {simValues[i]} confidence")
    