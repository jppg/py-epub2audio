#!/usr/bin/env python3
"""
Example Python script that shows how to use edge-tts as a module
"""
import edge_tts
import os
import re 

class Text2Speech:

   async def convert(input_voice):
      """
      Main function
      """
      print("Convert book with voice", input_voice)
      
      home_path = "output"

      lst_files = [s for s in os.listdir(home_path)
         if os.path.isfile(os.path.join(home_path, s))]
      lst_files.sort(key=lambda s: os.path.getctime(os.path.join(home_path, s)))

      for filename in lst_files:
         file_path = os.path.join(home_path, filename)
         #print(file_path, os.path.getctime(file_path))
         
         if os.path.isfile(file_path) and re.search('.txt', file_path):
            communicate = edge_tts.Communicate()
            print(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
               lines = f.read()

            #print(lines)
            #lines = input("What do you want TTS to say? ")
            
            
            #with tempfile.NamedTemporaryFile(delete=False, dir='.\\output', suffix='.mp3') as temporary_file:
            with open('.\\output\\record.mp3', 'ab') as temporary_file:
               print("Converting", filename)
               #https://docs.microsoft.com/en-US/azure/cognitive-services/speech-service/language-support
               async for i in communicate.run(lines, voice=input_voice):
                  if i[2] is not None:
                     temporary_file.write(i[2])
      print("End")