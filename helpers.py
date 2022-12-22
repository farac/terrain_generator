from locale import normalize
import PySimpleGUI as sg
from enum import Enum
import perlin_noise as p_n
import opensimplex as simplex
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
from PIL import Image, ImageColor

class Colors:
    Sea = (0,115,184)

    Salt_desert = (242,251,199)
    Grasslands = (154,205,50)
    Jungle = (107,141,8)
    Rainforest = (107,122,52)

    Desert = (244,191,30)
    Forest = (94,184,21)

    Grayrock = (188,188,188)
    Snow = (243,241,234)

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
        #all ranges are -1 to 1
        #all variables represent the end of range for height/moisture value
        #Sea, Lowlands, Plains, Hills, Mountains
        #Very_dry, Dry, Temperate, Wet, Very_wet
        #Very dry is lowest and not used
        self.Mountains = 1
        self.Sea = sealevel
        __, self.Lowlands, self.Plains, self.Hills, __ = np.linspace(self.Sea, self.Mountains, 5)

        self.Very_dry = -1
        self.Very_wet = 1
        self.Temperate = moisture_midpoint
        __, self.Dry, __ = np.linspace(self.Very_dry, self.Temperate, 3)
        __, self.Wet, __ = np.linspace(self.Temperate, self.Very_wet, 3)

    def populate_map(self, height, moisture):
        #height = x[0]
        #moisture = x[1]
        map_array = np.zeros(height.shape())
        for h,m in np.nditer([height, moisture]):
            if h <= self.Sea:
                return Colors.Sea
            elif h <= self.Lowlands:
                if m <= self.Dry: return Colors.Salt_desert
                if m <= self.Temperate: return Colors.Grasslands
                if m <= self.Wet: return Colors.Jungle
                if m <= self.Very_wet: return Colors.Rainforest
            elif h <= self.Plains:
                if m <= self.Dry: return Colors.Desert
                if m <= self.Temperate: return Colors.Forest
                if m <= self.Wet: return Colors.Jungle
                if m <= self.Very_wet: return Colors.Rainforest
            elif h <= self.Hills:
                if m <= self.Dry: return Colors.Grayrock
                if m <= self.Temperate: return Colors.Forest
                if m <= self.Wet: return Colors.Jungle
                if m <= self.Very_wet: return Colors.Rainforest
            elif h <= self.Mountains:
                if m <= self.Dry: return Colors.Grayrock
                if m <= self.Wet: return Colors.Snow
        return map_array

    # def create_from_noisemaps(self, heightmap, moisturemap):
    #     #ne ovako ovo je iteracija oba arraya istovremeno, i spremanje u treci
    #     #nova matrica u koju spremas rezultat bla bla
    #     for height_val in np.nditer(heightmap):
    #         for moisture_val in np.nditer(moisturemap):
    #             if(height_val < self.Sea):



