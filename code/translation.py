import os
import time
from ai import chat_gpt

class Translation:

    def translate_text(text):
        MAX_RETRIES = 10
        chatgpt_messages = []
        prompt = "[Translate the text to portuguese from Portugal. Use style transfer to make the translated text suitable for a book reader]"
        chatgpt_messages.append({"role": "user", "content": prompt})
        chatgpt_messages.append({"role": "system", "content": text})
        end = False
        retry = 0
        output = 'Empty'
        while not end:
            try:
                output = chat_gpt(chatgpt_messages)
                end = True
            except Exception as ex:
                time.sleep(10)
                retry = retry + 1
                print(retry, "Error in translation")
                if retry > MAX_RETRIES:
                    end = True

        #print(output)
        return output
            
        
