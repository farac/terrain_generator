import PySimpleGUI as sg
from PIL import Image

from helpers import Generator, Helper

sg.theme("DarkAmber")

heightmap_column = [[sg.Text("Heightmap:")],
          [sg.Text("A1 scale: "), sg.Input(key="-SCALE1-", size=3, default_text="60"),
           sg.Text("A1 weight: "), sg.Slider(key="-AMPL1-" ,range=(0,2), resolution=0.01, orientation='h')],
          [sg.Text("A2 scale: "), sg.Input(key="-SCALE2-", size=3, default_text="50"),
           sg.Text("A2 weight: "), sg.Slider(key="-AMPL2-" ,range=(0,2), resolution=0.01, orientation='h')],
          [sg.Text("A3 scale: "), sg.Input(key="-SCALE3-", size=3, default_text="40"),
           sg.Text("A3 weight: "), sg.Slider(key="-AMPL3-" ,range=(0,2), resolution=0.01, orientation='h')],
          [sg.Text("A4 scale: "), sg.Input(key="-SCALE4-", size=3, default_text="20"),
           sg.Text("A4 weight: "), sg.Slider(key="-AMPL4-" ,range=(0,2), resolution=0.01, orientation='h')],
          [sg.Text("A5 scale: "), sg.Input(key="-SCALE5-", size=3, default_text="10"),
           sg.Text("A5 weight: "), sg.Slider(key="-AMPL5-" ,range=(0,2), resolution=0.01, orientation='h')]]

tempmap_column = [[sg.Text("Moisture map:")],
          [sg.Text("A1 scale: "), sg.Input(key="-M_SCALE1-", size=3, default_text="60"),
           sg.Text("A1 weight: "), sg.Slider(key="-M_AMPL1-" ,range=(0,2), resolution=0.01, orientation='h')],
          [sg.Text("A2 scale: "), sg.Input(key="-M_SCALE2-", size=3, default_text="50"),
           sg.Text("A2 weight: "), sg.Slider(key="-M_AMPL2-" ,range=(0,2), resolution=0.01, orientation='h')],
          [sg.Text("A3 scale: "), sg.Input(key="-M_SCALE3-", size=3, default_text="40"),
           sg.Text("A3 weight: "), sg.Slider(key="-M_AMPL3-" ,range=(0,2), resolution=0.01, orientation='h')],
          [sg.Text("A4 scale: "), sg.Input(key="-M_SCALE4-", size=3, default_text="20"),
           sg.Text("A4 weight: "), sg.Slider(key="-M_AMPL4-" ,range=(0,2), resolution=0.01, orientation='h')],
          [sg.Text("A5 scale: "), sg.Input(key="-M_SCALE5-", size=3, default_text="10"),
           sg.Text("A5 weight: "), sg.Slider(key="-M_AMPL5-" ,range=(0,2), resolution=0.01, orientation='h')]]

map_image = sg.Image("test.png")
layout = [[map_image],      
          [sg.Text("Height: "), sg.Input(key="-HEIGHT-", size=6, default_text="256"), sg.Text("px")],
          [sg.Text("Width: "), sg.Input(key="-WIDTH-", size=6, default_text="400"), sg.Text("px")], 
          [sg.Text("Seed: "), sg.Input(key="-SEED-", size=12, default_text="123456789")],   
          [sg.Column(heightmap_column), sg.VSeperator(), sg.Column(tempmap_column)],
          [sg.Button("Generate"), sg.Button("Exit")],
          [sg.Text(key="-ERROR-", text_color="red")]]      

window = sg.Window('Map generator', layout)    
window.move_to_center

while True:
    event, values = window.read()
    window['-ERROR-'].update("")
    print(event, values)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Generate':
        if not Helper.check_strings_not_empty((values['-HEIGHT-'], values['-WIDTH-'])):
            Helper.print_error(window, "No dimension can be blank!")
            continue
        
        try:
            width = int(values['-WIDTH-'])
            height = int(values['-HEIGHT-'])
            seed = int(values['-SEED-'])
            a1_scale = int(values['-SCALE1-'])
            a2_scale = int(values['-SCALE2-'])
            a3_scale = int(values['-SCALE3-'])
            a4_scale = int(values['-SCALE4-'])
            a5_scale = int(values['-SCALE5-'])
        except ValueError:
            Helper.print_error(window, "Casting values to int failed, check input!")
            continue

        if height == 0 or width == 0:
            Helper.print_error(window, "No dimension can be equal to 0!")
            continue 

        if not (values['-AMPL1-'] or values['-AMPL2-'] or values['-AMPL3-'] or values['-AMPL4-'] or values['-AMPL5-']):
            Helper.print_error(window, "At least one heightmap amplitude weight must not be 0!")
            continue

        Generator.generate_heightmap(width, height, seed, 
                                     values['-AMPL1-'], values['-AMPL2-'], values['-AMPL3-'],
                                     values['-AMPL4-'], values['-AMPL5-'],
                                     a1_scale, a2_scale, a3_scale, a4_scale, a5_scale)

        #map_image.update("map.png")
        print("Done.")
window.close()