import os
from pathlib import Path
from pypdf import PdfReader
from ocr import Ocr
import pdf2image


class Pdf:
    HOME_PATH = "output"
    title = ""
    author = ""

    def __init__(self):
        os.makedirs(self.HOME_PATH, exist_ok=True)

    def convert_pdf_to_txt(self, ebook_path, ocr=False, lang='por'):
        filename = Path(ebook_path).stem
        pdffileobj=open(ebook_path,'rb')
        pdfreader = PdfReader(pdffileobj)
        meta = pdfreader.metadata
        self.author = meta.author
        self.title = meta.title

        if ocr:
            #Install Pdf2image 
            #this package depends from poppler, to install it -> https://blog.alivate.com.au/poppler-windows/
            #save it locally and set their path to your local environment variables~

            #Install 

            images = pdf2image.convert_from_path(ebook_path, dpi=400)

            ocr = Ocr()
            
            for pg in range(len(images)):
                pil_im = images[pg] # assuming that we're interested in the first page only
                img_file = os.path.join(self.HOME_PATH, "img_" + str(pg) + ".jpg")
                pil_im.save(img_file)

                text = ocr.get_text_from_image(img_file, lang)
                filename = "file_" + str(pg) + ".txt"
                output_file = open(os.path.join(self.HOME_PATH, filename),"a", encoding='utf-8')
                output_file.writelines(text)    

        else:
            file_count = 0
            n_pages=len(pdfreader.pages)
            for pg in range(n_pages):
                pageobj= pdfreader.pages[pg]
                text = pageobj.extract_text()
                filename = "file_" + str(file_count) + ".txt"
                output_file = open(os.path.join(self.HOME_PATH, filename),"a", encoding='utf-8')
                output_file.writelines(text)
                if pg % 10 == 0:
                    file_count += 1
        print("End")