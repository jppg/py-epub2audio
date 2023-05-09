import os
import cv2
import pytesseract
import numpy as np
from datetime import datetime
from PIL import Image

class Ocr:

    HOME_PATH = "output"

    def get_text_from_image_path(self, img_file_path, language='por'):
        img = cv2.imread(img_file_path)
        return self.get_text_from_image(img, language)

    def pre_proc_img(self, img):
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

        self.save_img(self, processed_img)

        return processed_img

    def save_img(self, img, tag=''):
        exec_date = datetime.now()
        exec_date_str = exec_date.strftime("%Y-%m-%d-%H%M%S")

        cv2.imwrite(os.path.join(self.HOME_PATH, tag + '_' + exec_date_str + ".png"), img)

    def pre_proc_img_a(self, img):
        img_resized_area = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        self.save_img(self, img_resized_area, 'resized_inter_area')

        img_resized_cubic = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        self.save_img(self, img_resized_cubic, 'resized_inter_cubic')

        img_resized_linear = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        self.save_img(self, img_resized_linear, 'resized_inter_linear')

        img = cv2.blur(img_resized_cubic,(5,5))
        self.save_img(self, img, 'blur')

        img = cv2.GaussianBlur(img, (5, 5), 0)
        self.save_img(self, img, 'gauss')

        img = cv2.medianBlur(img, 3)
        self.save_img(self, img, 'medianBlur')

        

    def get_text_from_image(self, img, language='por'):
        h, w, c = img.shape
        
        #processed_img = self.pre_proc_img_a(img)
        
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

        text = pytesseract.image_to_string(img, lang=language)
        #, config='--psm 3 --oem 2')
        #to further info about pytesseract configs --> https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc#config-files-and-augmenting-with-user-data
        #filename = "file_" + str(pg) + ".txt"
        #output_file = open(os.path.join(self.HOME_PATH, filename),"a", encoding='utf-8')
        return text
        