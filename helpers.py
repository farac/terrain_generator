from locale import normalize
import PySimpleGUI as sg
import perlin_noise as p_n
import opensimplex
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img

class Helper:

    def print_error(window, error_string):
        window["-ERROR-"].update(error_string)

    def check_strings_not_empty(strings):
        for string in strings:
            if not string:
                return False
        return True

class Generator:

    def generate_perlin_array(x, y, seed):
        array = []
        opensimplex.seed(seed)
        noise = p_n.PerlinNoise(2, seed)

        for i in range (x):
            row = []
            for j in range (y):
                value = Generator.normalize_to_bound_ab(noise([i/x, j/y]), -np.sqrt((2/4)), np.sqrt((2/4)), 0, 255)
                row.append(value)
            array.append(row)
        

        image = plt.imshow(array, cmap="gray")
        plt.imsave("map.png", array, cmap="gray")
        image2 = img.imread("map.png")
        plt.show()
        print(image2)
        return(((array)))
    
    #def array_to_image(array):

    def normalize_to_bound_ab(x, x_min, x_max, a, b):
        y = ((b - a) * (x - x_min / x_max - x_min)) + a
        return int(y)
