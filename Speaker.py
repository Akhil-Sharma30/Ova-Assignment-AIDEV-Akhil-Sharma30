from gtts import gTTS
import pygame

def text_to_speech(text, lang='en'):
    # Create a text-to-speech object
    tts = gTTS(text=text, lang=lang)
    
    # Save the speech to a temporary file
    tts.save("output.mp3")
    
def speak_mp3(mp3_file="output.mp3"):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

