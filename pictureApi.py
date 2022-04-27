import os
from random import random
from PIL import Image, ImageDraw, ImageFilter
from matplotlib import pyplot as plt
import numpy as np
from util import *
import requests


spacer = 10
imageSize = 217

image_height = 5 * spacer + 4 * imageSize
image_width = 4 * spacer + 3 * imageSize


class LoadoutGenerator():
    def __init__(self, player):
        equip = player["Equipment"]
        self.__bag = equip["Bag"]
        self.__head = equip["Head"]
        self.__cape = equip["Cape"]
        self.__armour = equip["Armor"]
        self.__weapon = equip["MainHand"]
        self.__offWeapon = equip["OffHand"]
        self.__food = equip["Food"]
        self.__potion = equip["Potion"]
        self.__boots = equip["Shoes"]
        self.__mount = equip["Mount"]
        self.__picPaths = []

    def cleanupCache(self):
        for path in self.__picPaths:
            if os.path.exists(path):
                os.remove(path)

    def generateEmptyItem(self):
        fileName = Util.generateRandomPngTempPath()
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

    def fetchIcon(self, id) -> Image:
        imagePath = Util.generateRandomPngTempPath()
        if id is not None:
            endpoint = "https://render.albiononline.com/v1/item/{0}.png".format(
                str(id["Type"]))
            request = requests.get(endpoint)
            if request.status_code == 200:
                file = open(imagePath, "wb")
                file.write(request.content)
                file.close()
        else:
            imagePath = self.generateEmptyItem()
        img = Image.open(imagePath)
        return img

    def height(self):
        return image_height
    
    def width(self):
        return image_width

    def generate(self):
        basePath = Util.generateBasePic(image_height, image_width)
        base = Image.open(basePath)
        base.paste(self.fetchIcon(self.__bag), (spacer, spacer))
        base.paste(self.fetchIcon(self.__head),
                   (spacer + imageSize + spacer, spacer))
        base.paste(self.fetchIcon(self.__cape), (spacer + imageSize +
                                                 spacer + imageSize + spacer, spacer))
        base.paste(self.fetchIcon(self.__weapon),
                   (spacer, spacer + imageSize + spacer))
        base.paste(self.fetchIcon(self.__armour), (spacer + imageSize +
                                                   spacer, spacer + imageSize + spacer))
        if self.__offWeapon is not None:
            base.paste(self.fetchIcon(self.__offWeapon), (spacer + imageSize +
                                                          spacer + imageSize + spacer, spacer + imageSize + spacer))
        else:
            base.paste(self.fetchIcon(self.__weapon), (spacer + imageSize +
                                                       spacer + imageSize + spacer, spacer + imageSize + spacer))
        base.paste(self.fetchIcon(self.__food), (spacer, spacer + imageSize +
                                                 spacer + imageSize + spacer))
        base.paste(self.fetchIcon(self.__boots), (spacer + imageSize + spacer, spacer +
                                                  imageSize + spacer + imageSize + spacer))
        base.paste(self.fetchIcon(self.__potion), (spacer + imageSize +
                                                   spacer + imageSize + spacer, spacer + imageSize + spacer + imageSize + spacer))
        base.paste(self.fetchIcon(self.__mount), (spacer + imageSize + spacer, spacer +
                                                  imageSize + spacer + imageSize + spacer + imageSize + spacer))
        base.save(basePath, quality=95)
        return basePath

# o = LoadoutGenerator("", "", "", "", "", "", "", "", "", "")
# o.generate()
# o.fetchIcon("T4_OFF_HORN_KEEPER")
