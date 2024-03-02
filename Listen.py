import pyaudio
import wave

class Listen:

    # def Listen():
    #     filename = "recorded.wav"
    #     chunk = 1024
    #     FORMAT = pyaudio.paInt16
    #     audio = pyaudio.PyAudio()
    #     stream = audio.open(format=FORMAT, channels=1, rate=44100, input=True, frames_per_buffer=chunk)
    #     print("Listening...")

    #     frames = []
    #     recording_started = False
    #     try:
    #         while True:
    #             data = stream.read(chunk)
    #             frames.append(data)

    #             # Convert audio data to string for analysis
    #             audio_data_str = data.decode("utf-8", "ignore")

    #             # Check if the keyword is detected
    #             if "thank you" in audio_data_str.lower() and recording_started:
    #                 print("Recording stopped.")
    #                 break
                
    #             if "tommy" in audio_data_str.lower() and not recording_started:
    #                 print("Recording started...")
    #                 recording_started = True

    #             # Start saving frames when recording starts
    #             if recording_started:
    #                 print("Recording... (Say 'thank you' to stop)")
    #                 try:
    #                     while True:
    #                         data = stream.read(chunk)
    #                         frames.append(data)
    #                         audio_data_str = data.decode("utf-8", "ignore")
    #                         print(audio_data_str)
    #                         if "thank you" in audio_data_str.lower():
    #                             print("Recording stopped.")
    #                             break
    #                 except KeyboardInterrupt:
    #                     print("Recording stopped.")
    #                     break
    #     except KeyboardInterrupt:
    #         print("Listening stopped.")

    #     # Close the audio stream
    #     stream.stop_stream()
    #     stream.close()
    #     audio.terminate()

    #     # Save the recorded audio to a WAV file
    #     with wave.open(filename, 'wb') as wf:
    #         wf.setnchannels(1)
    #         wf.setsampwidth(audio.get_sample_size(FORMAT))
    #         wf.setframerate(44100)
    #         wf.writeframes(b''.join(frames))

    #     print(f"Audio saved as {filename}")
    #     return filename


    def Listen():
        filename = "recorded.wav"
        chunk = 1024
        FORMAT = pyaudio.paInt16
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=1, rate=44100, input=True, frames_per_buffer=chunk)
        print("Recording... (Press Ctrl+C to stop)")
        frames = []
        try:
            while True:
                data = stream.read(chunk)
                frames.append(data)
        except KeyboardInterrupt:
            print("Recording stopped.")

        # Close the audio stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the recorded audio to a WAV file
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(44100)
            wf.writeframes(b''.join(frames))

        print(f"Audio saved as {filename}")
        return filename

