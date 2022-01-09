import re
import os
import ebooklib
import zipfile
from ebooklib import epub
from bs4 import BeautifulSoup
from pathlib import Path

class Epub:

    HOME_PATH = "output"

    def __init__(self, ebook_path):
        os.makedirs(self.HOME_PATH, exist_ok=True)
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

        print(book.get_metadata('DC', 'title'))
        print(book.get_metadata('DC', 'creator'))
        print(book.get_metadata('DC', 'language'))

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