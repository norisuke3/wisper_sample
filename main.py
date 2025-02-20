import os
import pyaudio
import wave
import json
from dotenv import load_dotenv
import whisper

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 音声入力の設定
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

# 音声ファイルの保存
WAVE_OUTPUT_FILENAME = "output.wav"

# PyAudioオブジェクトの作成
p = pyaudio.PyAudio()

# ストリームの開始
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

# 音声データの記録
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

# ストリームの停止
stream.stop_stream()
stream.close()
p.terminate()

# 音声データの保存
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Whisperを使って文字起こし
model = whisper.load_model("tiny")
result = model.transcribe("output.wav")
print(result["text"])

print("音声ファイル output.wav を作成しました。")
print("文字起こし結果を出力しました。")