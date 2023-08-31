from setuptools import setup, find_packages

setup(
    name='py-epub2audio',
    version='0.1.0',
    packages=find_packages(include=['code', 'code.*']),
    install_requires=[
        'configparser',
        'beautifulsoup4',
        'wxpython',
        'EbookLib',
        'edge-tts',
        'pypdf',
        'pdf2image',
        #'numpy',
        #'cv2',
        'pytesseract',
        'pypdfium2',
        'nltk',
        'langchain',
        'doctran'
    ]
)