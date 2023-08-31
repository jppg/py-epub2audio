import openai
import os

def chat_gpt(input_messages):
    openai.api_key = os.environ['OPENAI_API_KEY']
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=input_messages
    )

    return completion.choices[0].message.content