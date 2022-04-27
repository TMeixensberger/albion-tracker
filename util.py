import random
import tempfile
import hashlib
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

class Util():
    @staticmethod
    def generateRandomPngTempPath():
        seed = random.randint(0, 187187)
        hash_object = hashlib.md5(str(seed).encode('utf-8'))
        name = hash_object.hexdigest()
        fileName = "{0}/{1}.png".format(tempfile.gettempdir(), str(name))
        return fileName

    @staticmethod
    def generateBasePic(height, width):
        fileName = Util.generateRandomPngTempPath()
        canvas = 1 * np.ones((height, width, 3), np.uint8)
        plt.imshow(canvas, interpolation='nearest')
        plt.imsave(fileName, canvas)
        img = Image.open(fileName)
        rgba = img.convert("RGBA")
        datas = rgba.getdata()
        newData = []
        for item in datas:
            newData.append((255, 255, 255, 0))
        rgba.putdata(newData)
        rgba.save(fileName, "PNG")
        return fileName