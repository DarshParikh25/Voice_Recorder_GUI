import os
import time
import pyaudio
import tkinter as tk
import wave
import threading

class VoiceRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(width=True, height=True)
        
        self.button_start = tk.Button(text="Start Recording", font=("Arial", 30, "bold"), command=self.click_handler)
        self.button_start.pack(pady=10)

        self.button_stop = tk.Button(text="Stop Recording", font=("Arial", 30, "bold"), command=self.stop_recording, state=tk.DISABLED)
        self.button_stop.pack(pady=10)

        self.button_save = tk.Button(text="Save Recording", font=("Arial", 30, "bold"), command=self._save_audio, state=tk.DISABLED)
        self.button_save.pack(pady=10)

        self.label = tk.Label(text="00:00:00")
        self.label.pack()

        self.recording = False
        self.frames = []

        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.stop_recording()
        else:
            self.recording = True
            self.button_start.config(text="Recording...", state=tk.DISABLED)
            self.button_stop.config(state=tk.NORMAL)
            self.button_save.config(state=tk.DISABLED)
            threading.Thread(target=self.record).start()

    def stop_recording(self):
        self.recording = False
        self.button_start.config(text="Start Recording", state=tk.NORMAL)
        self.button_stop.config(state=tk.DISABLED)
        self.button_save.config(state=tk.NORMAL)

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.frames = []
        start = time.time()
        while self.recording:
            data = stream.read(1024)
            self.frames.append(data)
            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")
        stream.stop_stream()
        stream.close()
        audio.terminate()

    def _save_audio(self):
        exists = True
        file_no = 1
        while exists:
            if os.path.exists(f"recording{file_no}.wav"):
                file_no += 1
            else:
                exists = False

        sound_file = wave.open(f"recording{file_no}.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(self.frames))
        sound_file.close()

VoiceRecorder()