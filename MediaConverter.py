import os
import sys

# -------------------------------------------------------
# Importing libraries 
# -------------------------------------------------------
try:
    import moviepy.editor as mp
except:
    os.system("pip install moviepy")
    import moviepy.editor as mp
# -------------------------------------------------------
try:
    import speech_recognition as sr 
except:
    os.system("pip install SpeechRecognition==2.1.3")    
    import speech_recognition as sr 
# -------------------------------------------------------
try:
    from pydub import AudioSegment
    from pydub.silence import split_on_silence
except:
    os.system("pip install pydub")
    from pydub import AudioSegment
    from pydub.silence import split_on_silence
# -------------------------------------------------------
import tkinter as tk
from tkinter import filedialog
# -------------------------------------------------------


class MediaConverter():
    help = """
    Converts Video to Audio and Audio to Text

    Options:
    -h      ==> This help text    
    -va     ==> Convert Video to Audio
                -va "<VIDEO_PATH>" "<AUDIO_PATH_WITH_NAME>" 
                -va "<VIDEO_PATH>" 
                -va     (Allows to choose a file)
    -at     ==> Convert Audio to Text
                -at "<AUDIO_PATH>" "<TXT_PATH_WITH_NAME>"
                -at "<AUDIO_PATH>"
                -at     (Allows to choose a file)
    -vt     ==> Convert Video to Text
                -vt "<VIDEO_PATH>" "<TXT_PATH_WITH_NAME>"
                -vt "<VIDEO_PATH>"
                -vt     (Allows to choose a file)
    """

    def __init__(self):
        pass

    def cleanFilePath(self, filePath):
        clean = filePath
        clean = clean.replace("\\", "/")
        return clean

    def convertVideoToAudio(self, videoPath=None, audioPath=None):
        """
        Converts Video to Audio:
            If no audioPath with name and extention specified, default to .wav file. 
        """
        if videoPath:
            # Insert Local Video File Path 
            # clip = mp.VideoFileClip(r"Video File")
            videoPath = self.cleanFilePath(videoPath)
            clip = mp.VideoFileClip(videoPath)
            
            # Insert Local Audio File Path
            # clip.audio.write_audiofile(r"Audio File")
            if audioPath:
                audioPath = self.cleanFilePath(audioPath)
            else:
                audioPath = videoPath
                audioPath = audioPath.replace(".mp4", ".wav")
                audioPath = audioPath.replace(".mov", ".wav")
                audioPath = audioPath.replace(".wmv", ".wav")
                audioPath = audioPath.replace(".flv", ".wav")
                audioPath = audioPath.replace(".avi", ".wav")
            clip.audio.write_audiofile(audioPath)
            return audioPath
        else:
            print("No Video File Specified")
            return None

    def convertAudioToText(self, audioPath=None, textPath=None):
        """
        Converts Audio to Text:
            ONLY .wav files accepted for audioPath
            If no textPath with name and extention specified, default to txt file. 
        """
        if audioPath:
            audioPath = self.cleanFilePath(audioPath)
            text = self.get_large_audio_transcription(audioPath)
            print(text)
            if textPath:
                textPath = self.cleanFilePath(textPath)
            else:
                textPath = audioPath
                textPath = textPath.replace(".wav", ".txt")
            f = open(textPath, "a")
            f.write(text)
            f.close()
            print("Saved To File")
            return textPath
        print("No Audio File Specified")
        return None

    # a function that splits the audio file into chunks
    # and applies speech recognition
    def get_large_audio_transcription(self, path):
        """
        Splitting the large audio file into chunks
        and apply speech recognition on each of these chunks
        """
        print("Convert Audio to Text (WAV)")
        # create a speech recognition object
        r = sr.Recognizer()
        # open the audio file using pydub
        sound = AudioSegment.from_wav(path)  
        # split audio sound where silence is 700 miliseconds or more and get chunks
        chunks = split_on_silence(sound,
            # experiment with this value for your target audio file
            min_silence_len = 500,
            # adjust this per requirement
            silence_thresh = sound.dBFS-14,
            # keep the silence for 1 second, adjustable as well
            keep_silence=500,
        )
        folder_name = "audio-chunks"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        print("Processing Chunks")
        # process each chunk 
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk
            with sr.AudioFile(chunk_filename) as source:
                audio_listened = r.record(source)
                # try converting it to text
                try:
                    text = r.recognize_google(audio_listened)
                except sr.UnknownValueError as e:
                    print("Error:", str(e))
                else:
                    text = f"{text.capitalize()}. "
                    print(chunk_filename, ":", text)
                    whole_text += text + "\n"
            os.remove(chunk_filename)
        # return the text for all chunks detected
        return whole_text



# ==============================================================================================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    # print("START")
    obj = MediaConverter()

    if len(sys.argv) > 1:
        videoPath = None
        audioPath = None
        textPath  = None
        if sys.argv[1] == "-h":
            print(MediaConverter().help)

        elif sys.argv[1] == "-va":
            print("va")
            if len(sys.argv) > 2:   videoPath = str(sys.argv[2])
            else:                   videoPath = filedialog.askopenfilename()
            if len(sys.argv) > 3:   audioPath = str(sys.argv[3])
            print(videoPath)
            obj.convertVideoToAudio(videoPath, audioPath)
    
        elif sys.argv[1] == "-at":
            print("at")
            if len(sys.argv) > 2:   audioPath = str(sys.argv[2])
            else:                   audioPath = filedialog.askopenfilename()
            if len(sys.argv) > 3:   textPath  = str(sys.argv[3])
            print(audioPath)
            obj.convertAudioToText(audioPath, textPath)

        elif sys.argv[1] == "-vt":
            print("vt")
            if len(sys.argv) > 2:   videoPath = str(sys.argv[2])
            else:                   videoPath = filedialog.askopenfilename()
            if len(sys.argv) > 3:   textPath  = str(sys.argv[3])
            print(videoPath)
            obj.convertAudioToText(obj.convertVideoToAudio(videoPath))
    else:
        print(MediaConverter().help)
    # obj = MediaConverter()
    # videoPath = "Online_1.mp4"
    # audioPath = "Online_1_AUDIO.wav"
    # textPath  = "Online_1_TEXT.txt"
    # obj.convertVideoToAudio(videoPath, audioPath)
    # obj.convertAudioToText(audioPath, textPath)
    # obj.convertAudioToText(obj.convertVideoToAudio(videoPath))
    print("DONE")
# ==============================================================================================
