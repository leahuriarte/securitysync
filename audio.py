import pyaudio
import wave
import speech_recognition as sr
import numpy as np
import pickle
import sklearn

speech_model, cv = pickle.load(open("speech.pkl", 'rb'))

def recordAudio(filename):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 5
    input_device_index=0

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input_device_index=input_device_index,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribeAudio(filename):
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
    
        audio_text = r.listen(source)

        try:
            # using google speech recognition
            text = r.recognize_google(audio_text)
            print(text)
            return text
        
        except:
            return ""
        
def runAudio(hate_language):
    for i in range(4):
        filename = "audio/output"+str(i)+".wav"
        recordAudio(filename)
        text = [transcribeAudio(filename)]
        #if something was spoken
        if text != [""]:
            #analyze speech for hate language
            textdata = cv.transform(text).toarray()
            print(type(textdata))
            sentiment = speech_model.predict(textdata)
            #if hate language detected, save in array for reporting
            if 1 in sentiment or 0 in sentiment:
                hate_language.append(textdata)