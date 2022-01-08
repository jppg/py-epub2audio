#!/usr/bin/env python3
"""
Example Python script that shows how to use edge-tts as a module
"""
import edge_tts
import os

class Text2Speech:
   async def convert():
      """
      Main function
      """
      home_path = "output"
      for filename in os.listdir(home_path):
         file_path = os.path.join(home_path, filename)
         print(file_path)
         
         if os.path.isfile(file_path):
            communicate = edge_tts.Communicate()
            with open(file_path, 'r', encoding='utf-8') as f:
               lines = f.read()

            #print(lines)
            #lines = input("What do you want TTS to say? ")
            
            
            #with tempfile.NamedTemporaryFile(delete=False, dir='.\\output', suffix='.mp3') as temporary_file:
            with open('.\\output\\record.mp3', 'ab') as temporary_file:
               print("Converting", filename)
               async for i in communicate.run(lines, voice="pt-PT-FernandaNeural"):
                  if i[2] is not None:
                     temporary_file.write(i[2])
      print("End")