#!/usr/bin/env python3
"""
Example Python script that shows how to use edge-tts as a module
"""

import asyncio
import tempfile

from playsound import playsound

import edge_tts


async def main():
    """
    Main function
    """
    communicate = edge_tts.Communicate()
    ask = input("What do you want TTS to say? ")
    with open('.\\output\\record.mp3', 'ab') as temporary_file:
        print("Converting", temporary_file)
        #https://docs.microsoft.com/en-US/azure/cognitive-services/speech-service/language-support
        async for i in communicate.run(ask, voice="pt-PT-RaquelNeural"):
            if i[2] is not None:
                temporary_file.write(i[2])


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())