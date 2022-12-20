from locale import normalize
import PySimpleGUI as sg
from enum import Enum
import perlin_noise as p_n
import opensimplex as simplex
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
from PIL import Image, ImageColor

class Elevation(Enum):
    Sea, Lowlands, Plains, Hills, Mountains = range(5)

class Moisture(Enum):
    Very_dry, Dry, Temperate, Wet, Very_wet = range(5)

class Helper:

    def print_error(window, error_string):
        window["-ERROR-"].update(error_string)

    def check_strings_not_empty(strings):
        for string in strings:
            if not string:
                return False
        return True

    def normalize_to_bound_ab(x, x_min, x_max, a, b):
        y = ((b - a) * (x - x_min / x_max - x_min)) + a
        return int(y)
    
    def value_to_height_enum(value):
        if value < 0.4:
            return Elevation.Sea
        elif value < 0.6:
            return Elevation.Lowlands
        elif value < 0.8:
            return Elevation.Plains
        elif value < 0.9:
            return Elevation.Hills
        elif value < 1:
            return Elevation.Mountains

    def value_to_moisture_enum(value):
        if value < 0.4:
            return Moisture.Very_dry
        elif value < 0.6:
            return Elevation.Dry
        elif value < 0.8:
            return Elevation.Temperate
        elif value < 0.9:
            return Elevation.Wet
        elif value < 1:
            return Elevation.Very_wet

class Generator:

    def __init__(self, width, height, seed):
        self.width = width
        self.height = height
        self.seed = seed

    def generate_heightmap(width, height, seed, 
                           a1_weight, a2_weight, a3_weight, a4_weight, a5_weight,
                           a1_scale, a2_scale, a3_scale, a4_scale, a5_scale):
        simplex.seed(seed)

        white = ImageColor.getrgb("#ffffff") #0-0.1
        gray = ImageColor.getrgb("#999999")
        dark_green = ImageColor.getrgb("#068a06")
        light_green = ImageColor.getrgb("#2edc2e")
        idk = ImageColor.getrgb("#acc91a")
        brown = ImageColor.getrgb("#a96a09")
        yellow = ImageColor.getrgb("#f3eb3d")
        light_blue = ImageColor.getrgb("#32dfe2")
        blue = ImageColor.getrgb("#1bb1e1")
        dark_blue = ImageColor.getrgb("#0f52a8")

        im = Image.new('RGB',(width, height))
        heightmap = np.empty((height, width), Elevation)
        for y in range (0, height):
            for x in range (0, width):

                ampl1 = a1_weight * simplex.noise2(x / a1_scale, y / a1_scale)
                ampl2 = a2_weight * simplex.noise2 (x / a2_scale, y / a2_scale) 
                ampl3 = a3_weight * simplex.noise2(x / a3_scale, y / a3_scale)
                ampl4 = a4_weight * simplex.noise2(x / a4_scale, y / a4_scale)
                ampl5 = a5_weight * simplex.noise2 (x / a5_scale, y / a5_scale) 


                pixel_val = (ampl1 + ampl2 + ampl3 + ampl4 + ampl5) / (a1_weight + a2_weight + a3_weight + a4_weight + a5_weight)
                #normalize the values to 1-0
                #ovo nema smisla ako ces im davat vrijednosti i na kraju pretvarat u sliku + temperature
                #also pribaci ga nazad u numpy impl radi performanci
                pixel_val = (pixel_val + 1) / (1+1)
                print(pixel_val)
                heightmap[y][x] = Helper.value_to_height_enum(pixel_val)
                print(heightmap[y][x])
                #if pixel_val < 0.4:
                    #im.putpixel((x, y), blue)
                #elif pixel_val < 0.6:
                    #im.putpixel((x, y), yellow)
                #elif pixel_val < 0.8:
                    #im.putpixel((x, y), light_green)
                #elif pixel_val < 0.9:
                    #im.putpixel((x, y), dark_green)
                #elif pixel_val < 1:
                    #im.putpixel((x, y), white)


                #color = int((pixel_val) * 128)
                #im.putpixel((x, y), color)

        #im = im.resize((width*2, height*2))
        #im.save("map.png")