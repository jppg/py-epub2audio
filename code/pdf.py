import os
from pathlib import Path
from pypdf import PdfReader
from ocr import Ocr
import pdf2image
import pypdfium2 as pdfium


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
            ocr = Ocr()

            #Install 
            print("start convert pdf to image")
            # option 1 - using pdf2image
            '''
            info = pdf2image.pdfinfo_from_path(ebook_path, userpw=None, poppler_path=None)
            maxPages = info["Pages"]
            for page in range(1, maxPages+1, 10): 
                images = pdf2image.convert_from_path(ebook_path, dpi=300, first_page=page, last_page = min(page+10-1,maxPages))
                #images = pdf2image.convert_from_path(ebook_path, dpi=300)
            '''
            #option 2 - using pdfium
            
            pdf = pdfium.PdfDocument(ebook_path)
            version = pdf.get_version()  # get the PDF standard version
            n_pages = len(pdf)  # get the number of pages in the document
            
            init_pg = 66
            for bloc in range(init_pg, n_pages, 10):
                page_indices = [i for i in range(bloc, min(bloc+10, n_pages))]
                renderer = pdf.render(
                    pdfium.PdfBitmap.to_pil,
                    page_indices = page_indices,
                    scale = 300/72,  # 300dpi resolution
                )

                for i, image in zip(page_indices, renderer):
                    #ValueError: Out-of-bounds page indices are prohibited.
                    img_file = os.path.join(self.HOME_PATH, "img_" + str(i) + ".jpg")
                    
                    image.save(img_file)
                    
                    text = ocr.get_text_from_image_path(img_file, lang)
                    filename = "file_" + str(i) + ".txt"
                    output_file = open(os.path.join(self.HOME_PATH, filename),"a", encoding='utf-8')
                    output_file.writelines(text)
            '''
            pil_im = images[pg] # assuming that we're interested in the first page only
            img_file = os.path.join(self.HOME_PATH, "img_" + str(pg) + ".jpg")
            pil_im.save(img_file)
            '''
            #text = ocr.get_text_from_image_path(img_file, lang)
            #filename = "file_" + str(i) + ".txt"
            #output_file = open(os.path.join(self.HOME_PATH, filename),"a", encoding='utf-8')
            #output_file.writelines(text)
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