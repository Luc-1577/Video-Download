from pytube import YouTube
import io
import os
from PIL import Image, ImageTk
import customtkinter as CT
import requests

class Conversor(CT.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('700x500')
        self.title('Conversor')
        self.minsize(500, 400)
        self.resizable(True, True)
        CT.set_appearance_mode('dark')
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.combobox = CT.CTkComboBox(self, width=130, values=['Mp3', 'Mp4'], justify='center', command=self.metho)
        self.combobox.grid(row=0, column=0, padx=0, pady=10, sticky='s', columnspan=2)
        self.combobox.set('Conversor type')
        self.combobox.configure(state='readonly')

        self.entry = CT.CTkEntry(self, corner_radius=10, width=500, placeholder_text="Paste the URL")
        self.entry.grid(row=3, column=0, padx=0, pady=20, sticky='e')  
        
        self.button = CT.CTkButton(self, text='Convert', corner_radius=10, command=self.show_thub)
        self.button.grid(row=3, column=1, padx=0, pady=0, sticky='w')
    
    def metho(self, choice):
        global method
        method = choice
        
    def get_thub(self, url):
        thub = YouTube(url).thumbnail_url
        
        info = requests.get(thub)
        img = Image.open(io.BytesIO(info.content))
        img = img.resize((400, 250), Image.LANCZOS)
        imgCTk = ImageTk.PhotoImage(img)
        return imgCTk
        
    def show_thub(self):
        self.url = self.entry.get()
        thub = self.get_thub(self.url)
        
        self.img = CT.CTkLabel(self, image=thub, text='')
        self.img.grid(row=1, column=0, padx=0, pady=0, sticky='sn', columnspan=2)
                
        self.download_btn = CT.CTkButton(self, text='Download', corner_radius=6, command=self.download)
        self.download_btn.grid(row=2, column=0, padx=0, pady=0, sticky='n', columnspan=2)         
    
    def download(self):
        dirpath = os.path.dirname(__file__)

        if method == 'Mp4':
            dirpath = os.path.join(dirpath, 'Video')
            os.makedirs(dirpath, exist_ok=True)
            
            video = YouTube(self.url).streams.get_highest_resolution()
            video.download(output_path=dirpath)
        
        elif method == 'Mp3':
            dirpath = os.path.join(dirpath, 'Mp3')
            os.makedirs(dirpath, exist_ok=True)

            audio = YouTube(self.url).streams.get_audio_only()

            file_name = audio.default_filename
            file, _ = os.path.splitext(file_name)
            file_name = os.path.join(dirpath, file_name)

            new_file = file + '.mp3'
            new_file = os.path.join(dirpath, new_file)

            if not os.path.exists(new_file):
                audio.download(output_path=dirpath)            
                os.rename(file_name, new_file)

Conversor().mainloop()