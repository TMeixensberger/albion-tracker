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


class Loadout():
    def __init__(self, player):
        equip = player["Equipment"]
        self.bag = equip["Bag"]
        self.head = equip["Head"]
        self.cape = equip["Cape"]
        self.armour = equip["Armor"]
        self.weapon = equip["MainHand"]
        if equip["OffHand"] is None:
            self.offWeapon = equip["MainHand"]
        else:
            self.offWeapon = equip["OffHand"]

        self.food = equip["Food"]
        self.potion = equip["Potion"]
        self.boots = equip["Shoes"]
        self.mount = equip["Mount"]
