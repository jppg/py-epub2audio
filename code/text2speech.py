#!/usr/bin/env python3
"""
Example Python script that shows how to use edge-tts as a module
"""
import edge_tts
import os
import re 
import json
from nltk.tokenize import sent_tokenize
import nltk

nltk.download('punkt')

class Text2Speech:

   async def convert(input_voice, title, author):
      """
      Main function
      """
      print("Convert book with voice", input_voice)
      
      home_path = "output"

      filename = title + " - " + author + ".mp3"
      filename = filename.replace(",", "")
      filename = filename.replace("?", "")
      filename = filename.replace("!", "")
      filename = filename.replace("*", "")

      say_title = True

      with open("replace_chars.json") as replace_chars_file:
         data_dict = json.load(replace_chars_file)

      lst_files = [s for s in os.listdir(home_path)
         if os.path.isfile(os.path.join(home_path, s))]
      lst_files.sort(key=lambda s: os.path.getctime(os.path.join(home_path, s)))

      for input_file in lst_files:
         print("Converting", input_file)
         file_path = os.path.join(home_path, input_file)
         
         if os.path.isfile(file_path) and re.search('.txt', file_path):
            communicate = edge_tts.Communicate()
            
            with open(file_path, 'r', encoding='utf-8') as f:
               lines = f.read()
               file_tk = ''
               if say_title:
                  file_tk = title + ' de ' + author + "\n"
                  say_title = False
                  
               for item in range(len(data_dict["chars"])):
                  lines = lines.replace(data_dict["chars"][item]["old"], data_dict["chars"][item]["new"])

               #https://docs.microsoft.com/en-US/azure/cognitive-services/speech-service/language-support
               with open('.\\output\\' + filename, 'ab') as temporary_file:
                  for tk in sent_tokenize(lines):
                     #file_tk += tk + '\n'
                     async for i in communicate.run(tk, voice=input_voice):
                        if i[2] is not None:
                           temporary_file.write(i[2])
      print("End")