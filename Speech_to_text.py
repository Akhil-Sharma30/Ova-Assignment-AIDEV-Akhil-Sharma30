import whisper
import Speaker as voice
from Listen import Listen
import Image_generation as i

# Listen and then text file

# Speech to Text
def Speech_to_text():
    audio_path = Listen.Listen()
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    print(result["text"])
    return result["text"]

# Text to Speech
result=Speech_to_text()

voice.text_to_speech(result)
voice.speak_mp3()
i.chatgpt((result))
