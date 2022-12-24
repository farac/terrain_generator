from locale import normalize
import PySimpleGUI as sg
from enum import Enum
import perlin_noise as p_n
import opensimplex as simplex
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import matplotlib.colors as col
from PIL import Image, ImageColor

class Colors:
    Sea = "#0073B8"

    Salt_desert = "#F2FBC7"
    Grasslands = "#9ACD32"
    Jungle = "#6B8D08"
    Rainforest = "#6B7A34"

    Desert = "#F4BF1E"
    Forest = "#5EB815"

    Grayrock = "#BCBCBC"
    Snow = "#F3F1EA"

    map_colors = col.ListedColormap((Sea, Salt_desert, Desert, Grasslands, Forest, Jungle, Rainforest, Grayrock, Snow))
    Sea_v, Salt_desert_v, Desert_v, Grasslands_v, Forest_v, Jungle_v, Rainforest_v, Grayrock_v, Snow_v = np.linspace(0, 1, 9)

class Helper:

    def print_error(window, error_string):
        window["-ERROR-"].update(error_string)

    def check_strings_not_empty(strings):
        for string in strings:
            if not string:
                return False
        return True

    def scale(data):
        #a=-1, b=1
        return (-1 - 1) * ((data - np.min(data)) / (np.max(data) - np.min(data))) + 1

    def fetch_random_int():
        rng = np.random.default_rng()
        return rng.integers(np.iinfo(np.int32).max)
    
    def random_int_from_seed(seed):
        rng = np.random.default_rng(seed)
        return rng.integers(np.iinfo(np.int32).max)

class Noise_Generator:

    def __init__(self, width, height, seed):
        self.width = width
        self.height = height
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        ##onapravi da se poziva novi unutar generacije 
        #mozes generirat seedove za njega i tjt, deterministicki je
    
    def generate_noise_array(self,
                             a1_weight, a2_weight, a3_weight, a4_weight, a5_weight,
                             a1_scale, a2_scale, a3_scale, a4_scale, a5_scale, is_moisture = False):
        # if not is_moisture:
        #     simplex.seed(self.seed)
        # else:
        #     simplex.seed(self.seed + 1)
        simplex.seed(self.rng.integers(np.iinfo(np.int32).max))
        ix, iy = np.arange(self.width), np.arange(self.height)

        ampl1 = a1_weight * (simplex.noise2array(ix / a1_scale, iy / a1_scale))
        ampl2 = a2_weight * (simplex.noise2array(ix / a2_scale, iy / a2_scale))
        ampl3 = a3_weight * (simplex.noise2array(ix / a3_scale, iy / a3_scale))
        ampl4 = a4_weight * (simplex.noise2array(ix / a4_scale, iy / a4_scale))
        ampl5 = a5_weight * (simplex.noise2array(ix / a5_scale, iy / a5_scale))

        noise_array = (ampl1 + ampl2 + ampl3 + ampl4 + ampl5) / (a1_weight + a2_weight + a3_weight + a4_weight + a5_weight)
        if not is_moisture:
            plt.imsave("height.png", noise_array, cmap="gray")
        else:
            plt.imsave("moisture.png", noise_array, cmap="gray")
        
        return Helper.scale(noise_array)

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
        size = height.shape
        map_array = np.zeros(size)
        it = np.nditer([height, moisture], flags=['multi_index'])
        for h,m in it:
            if h <= self.Sea:
                map_array[it.multi_index] = Colors.Sea_v
            elif h <= self.Lowlands:
                if m <= self.Dry: map_array[it.multi_index] = Colors.Salt_desert_v
                elif m <= self.Temperate: map_array[it.multi_index] = Colors.Grasslands_v
                elif m <= self.Wet: map_array[it.multi_index] = Colors.Jungle_v
                elif m <= self.Very_wet: map_array[it.multi_index] = Colors.Rainforest_v
            elif h <= self.Plains:
                if m <= self.Dry: map_array[it.multi_index] = Colors.Desert_v
                elif m <= self.Temperate: map_array[it.multi_index] = Colors.Forest_v
                elif m <= self.Wet: map_array[it.multi_index] = Colors.Jungle_v
                elif m <= self.Very_wet: map_array[it.multi_index] = Colors.Rainforest_v
            elif h <= self.Hills:
                if m <= self.Dry: map_array[it.multi_index] = Colors.Grayrock_v
                elif m <= self.Temperate: map_array[it.multi_index] = Colors.Forest_v
                elif m <= self.Wet: map_array[it.multi_index] = Colors.Jungle_v
                elif m <= self.Very_wet: map_array[it.multi_index] = Colors.Rainforest_v
            elif h <= self.Mountains:
                if m <= self.Dry: map_array[it.multi_index] = Colors.Grayrock_v
                elif m <= self.Wet: map_array[it.multi_index] = Colors.Snow_v
        return map_array