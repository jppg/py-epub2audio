#!/usr/bin/env python3

import json
import os
import re

import edge_tts
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

class Text2Speech:

   async def convert(input_voice, title, author):
      """
      Main function
      """
      print("Convert book with voice", input_voice)
      
      home_path = "output"

      mp3_filename = title + " - " + author + ".mp3"
      mp3_filename = mp3_filename.replace(",", "")
      mp3_filename = mp3_filename.replace("?", "")
      mp3_filename = mp3_filename.replace("!", "")
      mp3_filename = mp3_filename.replace("*", "")
      webvtt_filename = mp3_filename[:-len(".mp3")] + ".vtt"

      say_title = True

      with open("replace_chars.json") as replace_chars_file:
         data_dict = json.load(replace_chars_file)

      lst_files = [s for s in os.listdir(home_path)
         if os.path.isfile(os.path.join(home_path, s))]
      lst_files.sort(key=lambda s: os.path.getctime(os.path.join(home_path, s)))

      file_tk = ''
      for input_file in lst_files:
         file_path = os.path.join(home_path, input_file)
         if os.path.isfile(file_path) and re.search(r'\.txt$', file_path):
            print("Converting", input_file)
            with open(file_path, 'r', encoding='utf-8') as f:
               lines = f.read()
               if say_title:
                  file_tk += title + ' de ' + author + "\n"
                  say_title = False
                  
               for item in range(len(data_dict["chars"])):
                  lines = lines.replace(data_dict["chars"][item]["old"], data_dict["chars"][item]["new"])

               for tk in sent_tokenize(lines):
                  file_tk += tk + '\n'

               # Add extra newline to signal new paragraph to TTS
               file_tk += '\n'

      #https://docs.microsoft.com/en-US/azure/cognitive-services/speech-service/language-support
      communicate = edge_tts.Communicate(file_tk, input_voice)
      submaker = edge_tts.SubMaker()
      with open(os.path.join('output', mp3_filename), "wb") as file:
         async for chunk in communicate.stream():
            if chunk["type"] == "audio":
               file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
               submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

      with open(os.path.join('output', webvtt_filename), "w", encoding='utf-8') as file:
         file.write(submaker.generate_subs())
      print("End")