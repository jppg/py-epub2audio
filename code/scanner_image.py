import os
import re
from pathlib import Path
from ocr import Ocr

class ScannerImage:
    HOME_PATH = "output"
    title = ""
    author = ""

    

    def convert_img_to_txt(self, lang='por'):
        lst_files = [s for s in os.listdir(self.HOME_PATH)
            if os.path.isfile(os.path.join(self.HOME_PATH, s))]
        lst_files.sort(key=lambda s: os.path.getctime(os.path.join(self.HOME_PATH, s)))
        
        ocr = Ocr()

        for input_file in lst_files:
            print("Converting", input_file)
            file_path = os.path.join(self.HOME_PATH, input_file)
            
            if os.path.isfile(file_path) and re.search('.png', file_path):    
                text = ocr.get_text_from_image_path(file_path, lang)
                filename = os.path.basename(file_path).replace('.png', '.txt')
                output_file = open(os.path.join(self.HOME_PATH, filename),"a", encoding='utf-8')
                output_file.writelines(text)