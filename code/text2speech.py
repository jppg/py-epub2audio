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
from translation import Translation
import langid

nltk.download('punkt')
MAX_WORDS = 1000

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
      #lst_files.sort(key=lambda s: os.path.join(home_path, s))
      lst_files.sort(key=lambda s: os.path.getmtime(os.path.join(home_path, s)))

      for input_file in lst_files:
         print("Converting", input_file)
         file_path = os.path.join(home_path, input_file)
         
         if os.path.isfile(file_path) and re.search('.txt', file_path):
            communicate = edge_tts.Communicate()
            
            with open(file_path, 'r', encoding='utf-8') as f:
               lines = f.read()

               lang = langid.classify(lines)
               
               file_tk = ''
               if say_title:
                  file_tk = title + ' de ' + author + "\n"
                  say_title = False
                  
               for item in range(len(data_dict["chars"])):
                  lines = lines.replace(data_dict["chars"][item]["old"], data_dict["chars"][item]["new"])

               
               
               #https://docs.microsoft.com/en-US/azure/cognitive-services/speech-service/language-support
               with open(os.path.join(home_path, filename), 'ab') as temporary_file:
                  idx = 0
                  text_chunk = ''
                  paragraph_list = sent_tokenize(lines)
                  
                  for paragraph in paragraph_list:
                     idx = idx + 1
                     text_chunk += paragraph + ' '
                     n_words = len(text_chunk.split(' '))
                     if n_words > MAX_WORDS or idx == len(paragraph_list):
                        if not input_voice.startswith(lang[0]):
                           print("Before >> ", text_chunk)
                           text_chunk = Translation.translate_text(text_chunk)
                           print("After Translation >> ", text_chunk)

                        async for i in communicate.run(text_chunk, voice=input_voice):
                           if i[2] is not None:
                              temporary_file.write(i[2])
                        text_chunk = ''
               
      print("End")