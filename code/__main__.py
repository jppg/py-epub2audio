from newspaper import Article
import nltk
from gtts import gTTS
import os

article = Article('https://hackernoon.com/future-of-python-language-bright-or-dull-uv41u3xwx')

article.download()

article.parse()

nltk.download('punkt')

article.nlp()

mytext = article.text

language = 'en' #English

myobj = gTTS(text=mytext, lang=language, slow=False)

myobj.save("read_article.mp3")