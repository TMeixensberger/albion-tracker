import random
import tempfile
import hashlib
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import os.path

import requests


class Util():
    @staticmethod
    def generateRandomPngTempPath():
        seed = random.randint(0, 187187)
        hash_object = hashlib.md5(str(seed).encode('utf-8'))
        name = hash_object.hexdigest()
        fileName = "{0}/{1}.png".format(tempfile.gettempdir(), str(name))
        return fileName

    @staticmethod
    def getTmpImgPath(imageName):
        return "{0}/{1}.png".format(tempfile.gettempdir(), str(imageName))

    @staticmethod
    def getEmptyItem():
        fileName = Util.getTmpImgPath("emptyItem")
        if os.path.exists(fileName):
            return fileName
        else:
            imageSize = 217
            canvas = 1 * np.ones((imageSize, imageSize, 3), np.uint8)
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

    @staticmethod
    def fetchIcon(item) -> Image:
        if item is not None:
            iconPath = Util.getTmpImgPath(item["Type"])
            if not os.path.exists(iconPath):
                endpoint = "https://render.albiononline.com/v1/item/{0}.png".format(
                    str(item["Type"]))
                request = requests.get(endpoint)
                if request.status_code == 200:
                    file = open(iconPath, "wb")
                    file.write(request.content)
                    file.close()
            return Image.open(iconPath)
        else:
            return Image.open(Util.getEmptyItem())
