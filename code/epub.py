import re
import os
import ebooklib
import zipfile
from ebooklib import epub
from bs4 import BeautifulSoup
from pathlib import Path
from pypdf import PdfReader
import pdf2image
import cv2
import pytesseract
import numpy as np

class Epub:

    HOME_PATH = "output"
    title = ""
    author = ""

    def __init__(self):
        os.makedirs(self.HOME_PATH, exist_ok=True)

    def convert2Txt(self, ebook_path):
        file_extension = Path(ebook_path).suffix
        if file_extension == '.pdf':
            self.convert_pdf_to_txt(ebook_path)
        else:
            try:
                self.open_epub_file(ebook_path)
            except Exception as e:
                print("Try to open file as zip")
                self.open_epub_file_as_zip(ebook_path)

    def open_epub_file_as_zip(self, ebook_path):
        with zipfile.ZipFile(ebook_path, 'r') as zip_ref:
            zip_ref.extractall(self.HOME_PATH)
            text_directory = os.path.join(self.HOME_PATH, 'ODIN//Text')
            for filename in os.listdir(text_directory):
                file_path = os.path.join(text_directory, filename)
                print(file_path)
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        filename = Path(file_path).stem
                        html = f.read()
                        self.convert_html_to_txt(filename, html)
                
    def open_epub_file(self, ebook_path):
        book = epub.read_epub(ebook_path)

        self.title = book.get_metadata('DC', 'title')
        self.author = book.get_metadata('DC', 'creator')
        #print(book.get_metadata('DC', 'language'))

        count = 0

        for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            count = count + 1
            html = doc.get_content()
            part_name = doc.get_name()
            part_name = part_name.replace('/','')
            print(count, '/', part_name)

            self.convert_html_to_txt(part_name, html)

    def convert_html_to_txt(self, filename, html):
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        raw = soup.get_text()
        raw = raw.replace(filename, '')

        file_to_save = filename

        if len(raw) < 2000:
            file_to_save = file_to_save + '-exc'

        file_to_save = os.path.join(self.HOME_PATH, file_to_save + ".txt")
        
        #sentence tokenize
        #from nltk.tokenize import sent_tokenize
        #mytext = "Bonjour M. Adam, comment allez-vous? J'espère que tout va bien. Aujourd'hui est un bon jour."
        #print(sent_tokenize(mytext,"french"))
        
        with open(file_to_save, 'w', encoding='utf-8') as f:
            f.write(raw)
        print("End")

    def convert_pdf_to_txt(self, ebook_path):
        filename = Path(ebook_path).stem
        pdffileobj=open(ebook_path,'rb')
        pdfreader = PdfReader(pdffileobj)
        meta = pdfreader.metadata
        self.author = meta.author
        self.title = meta.title

        if self.author == "CamScanner":
            #Install Pdf2image 
            #this package depends from poppler, to install it -> https://blog.alivate.com.au/poppler-windows/
            #save it locally and set their path to your local environment variables~

            #Install 

            images = pdf2image.convert_from_path(ebook_path, dpi=400)
            
            for pg in range(len(images)):
                pil_im = images[pg] # assuming that we're interested in the first page only
                img_file = os.path.join(self.HOME_PATH, "img_" + str(pg) + ".jpg")
                pil_im.save(img_file)

                img = cv2.imread(img_file)

                h, w, c = img.shape
                
                #Preprocessing image
                #https://tesseract-ocr.github.io/tessdoc/ImproveQuality

                #Read and prepare image
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (7, 7), 0)

                # Binarization appling adaptive thresholding
                mask = cv2.adaptiveThreshold(blurred, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)                
                #mask = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10)
                #mask = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 10)
                
                #Dilation and Erosion
                kernel = np.ones((2,2),np.uint8)
                processed_img = cv2.erode(mask, kernel, iterations = 1)
                processed_img = cv2.dilate(processed_img, kernel, iterations = 1)

                cv2.imwrite(os.path.join(self.HOME_PATH, "img_processed_" + str(pg) + ".jpg"), processed_img)
                
                #[+more details] 
                # https://pyimagesearch.com/2021/05/12/adaptive-thresholding-with-opencv-cv2-adaptivethreshold/ 
                # https://towardsdatascience.com/pre-processing-in-ocr-fc231c6035a7

                #To install Tesseract
                #choco install tesseract
                #If the package is not installed in the C:\Program Files\Tesseract-OCR folder please check the folder C:\ProgramData\chocolatey\lib\tesseract\tools
                #Extract the file tesseract-ocr-w64-setup-v5.3.0.20221214.exe as a zip file and copy them to your local applications folder
                #Add this folder to your PATH environment variables
                #In the end get the portuguese language model from here https://github.com/tesseract-ocr/tessdata find by por.traineddata and save in your application folder C:\Applics\tesseract-ocr-w64-setup-v5.3.0.20221214\tessdata

                #ocr_dict = pytesseract.image_to_data(pil_im, lang='por', output_type=Output.DICT)
                # ocr_dict now holds all the OCR info including text and location on the image
                #text = " ".join(ocr_dict['text'])

                text = pytesseract.image_to_string(processed_img, lang='por')
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

    def get_author(self):
        return self.author

    def get_title(self):
        return self.title