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

    def scale(data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))

class Noise_Generator:

    def __init__(self, width, height, seed):
        self.width = width
        self.height = height
        self.seed = seed
    
    def generate_noise_array(self,
                             a1_weight, a2_weight, a3_weight, a4_weight, a5_weight,
                             a1_scale, a2_scale, a3_scale, a4_scale, a5_scale):
        simplex.seed(self.seed)
        ix, iy = np.arange(self.width), np.arange(self.height)

        ampl1 = a1_weight * Helper.scale(simplex.noise2array(ix / a1_scale, iy / a2_scale))
        ampl2 = a2_weight * Helper.scale(simplex.noise2array(ix / a2_scale, iy / a2_scale))
        ampl3 = a3_weight * Helper.scale(simplex.noise2array(ix / a3_scale, iy / a3_scale))
        ampl4 = a4_weight * Helper.scale(simplex.noise2array(ix / a4_scale, iy / a4_scale))
        ampl5 = a5_weight * Helper.scale(simplex.noise2array(ix / a5_scale, iy / a5_scale))

        noise_array = (ampl1 + ampl2 + ampl3 + ampl4 + ampl5) / (a1_weight + a2_weight + a3_weight + a4_weight + a5_weight)
        plt.imsave("map.png", noise_array, cmap="gray")
        
        return noise_array

class Map:
    def __init__(self, sealevel, moisture_midpoint):
        self.sealevel = sealevel
        self.moisture_midpoint = moisture_midpoint

    def create_from_noisemaps(self, height, moisture):
        
