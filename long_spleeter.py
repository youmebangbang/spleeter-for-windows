import subprocess
import os
import shutil
import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import get_value
from pydub import AudioSegment

dpg.create_context()

class Spleet:
    def __init__(self):
        self.spleeter_audio_path = None

    def set_audio_path(self, path):
        self.spleeter_audio_path = path

    def get_audio_path(self):
        return self.spleeter_audio_path

spleet = Spleet()

def spleeter_update_status(text):
    text = dpg.get_value("spleeter_status_text") + text   
    dpg.set_value("spleeter_status_text", text)
    dpg.set_y_scroll("spleeter_status_window", 1000000)     

def callback_spleeter_open_audio(sender, app_data):
    d_path = app_data["selections"]
    key = list(d_path.keys())[0]
    path = app_data["selections"][key]
    spleet.set_audio_path(path)
    spleeter_update_status(f"\n\nFile {path} opened.")

def callback_spleeter_run(sender, data):
    project_folder = dpg.get_value("spleeter_project_folder")
    os.makedirs(f"{project_folder}/spleeter_out", exist_ok=True)
    path = spleet.get_audio_path()
    if not path:
        print("audio not selected")
        return
        
    a = AudioSegment.from_wav(path)
    count = 0
    while a:
        spleeter_update_status(f"\n\nProcessing cut {count}.")
        split = a[:600000]
        a = a[600000:]
        split.export(project_folder + "/spleeter_out/" + str(count) + ".wav", format='wav')
        
        spleeter_process =  subprocess.run(['python', '-m', 'spleeter', 'separate', '-p', 'spleeter:2stems', '-o', project_folder + '/spleeter_out/spleeter_' + str(count), project_folder + '/spleeter_out/' + str(count) + '.wav'] , stdout=subprocess.PIPE)  
        count += 1


with dpg.window(tag='spleeter_window', width=1400, height=800):

    with dpg.file_dialog(modal=True, width=800, directory_selector=False, show=False, callback=callback_spleeter_open_audio, tag="spleeter_open_audio_dialog"):
        dpg.add_file_extension(".*", color=(255, 255, 255, 255)) 

    dpg.add_spacer(height=10)
    dpg.add_input_text(tag="spleeter_project_folder", label="Project name", default_value="MyProject", width=150)
    dpg.add_spacer(height=10)
    dpg.add_button(tag="spleeter_choose_audio", label="Choose audio file", callback=lambda: dpg.show_item("spleeter_open_audio_dialog"))
    dpg.add_spacer(height=10)
    dpg.add_button(tag="spleeter_run", label="Run spleeter", callback=callback_spleeter_run)

    with dpg.window(tag="spleeter_status_window", no_background=True, show=True, pos=(5,300), width=800, height=400, menubar=False, no_resize=True, no_title_bar=True, no_move=True, no_scrollbar=True, no_collapse=True, no_close=True):     
        dpg.add_text(tag="spleeter_status_text", default_value="Status...")
    
with dpg.font_registry():
    default_font = dpg.add_font("CheyenneSans-Light.otf", 17)
    font2 = dpg.add_font("PublicSans-Regular.otf", 18)
    font3 = dpg.add_font("VarelaRound-Regular.ttf", 17)
    
dpg.bind_font(font2)

with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (7, 18, 54), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (59, 58, 68), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

dpg.create_viewport(title="Long Spleeter by YouMeBangBang", width=1400, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_global_font_scale(1.0)

dpg.set_primary_window("spleeter_window", True)
dpg.start_dearpygui()
dpg.destroy_context()