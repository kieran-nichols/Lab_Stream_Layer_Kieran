# -*- coding: utf-8 -*-
"""
Created on 28.10.2022.
@author: Kieran Nichols
"""

import cv2
import os
import sys
import time
import numpy as np
import pyaudio
import wave
import threading
from datetime import datetime
from pylsl import StreamInfo, StreamOutlet
import moviepy.editor as mp
import uuid

def createOutlet(stream_name, channel_names, videoFile):
    info = StreamInfo(name=stream_name,
                      type='StringStream',
                      channel_format='string',
                      channel_count=len(channel_names),
                      source_id=str(uuid.uuid4()))

    dir_file = os.path.dirname(videoFile)
    if not os.path.exists(dir_file):
        print('Creating folder', dir_file)
        os.makedirs(dir_file)

    # Optionally, you can set channel names in the description
    chns = info.desc().append_child("channels")
    for name in channel_names:
        chn = chns.append_child("channel")
        chn.append_child_value("label", name)
        
    info.desc().append_child_value("videoFile", videoFile)
    return StreamOutlet(info)

# Audio recording function
def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == "__main__":
    dir_out = os.path.dirname(os.path.realpath(__file__))
    dev = 1
    new_fps = int(30)
    cap = cv2.VideoCapture(dev)
    if not cap.isOpened():
        print("Cannot open camera")
        sys.exit()
    ret, frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # adj_height, adj_width = int(2160), int(3840) # 4K # the video seems to be faster than audio
    adj_height, adj_width = int(720), int(1280) # 2K
    # adj_height, adj_width = int(540), int(960) # 1K   
    
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    cap.open(dev, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FOURCC, fourcc) 
    cap.set(cv2.CAP_PROP_FPS, new_fps)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, adj_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, adj_height)
    
    str_datetime = datetime.now().strftime("_%Y%m%d_%H%M")
    filename = os.path.join(dir_out, 'Camera' + str(dev) + str_datetime + '.avi')
    out = cv2.VideoWriter(filename, fourcc, new_fps, (adj_width, adj_height))
    
    outlet = createOutlet('video_data', ['frame_num', 'time in ms'], filename)
    
    # Audio recording setup
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "output_audio.wav"
    recording = True
    audio_thread = threading.Thread(target=record_audio)
    audio_thread.start()
    
    frameCounter = 1
    start_time = time.time()
    old_time = time.perf_counter()
    
    while True:
        ret, frame = cap.read(cv2.CAP_DSHOW)
        if ret:
            new_time = time.time()
            elapsed_time1 = new_time - start_time
            elapsed_time_str = f"{elapsed_time1:.2f} s"
            text_to_display = f"Time: {elapsed_time_str} Frame Num: {frameCounter}"
            cv2.putText(frame, text_to_display, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            out.write(frame)
            outlet.push_sample([str(frameCounter), elapsed_time_str])
            cv2.imshow('Press q to end.', frame)
            frameCounter += 1
        
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            break
    
    recording = False
    audio_thread.join()
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    # Combine video and audio using MoviePy
    video = mp.VideoFileClip(filename)
    audio = mp.AudioFileClip(WAVE_OUTPUT_FILENAME)
    final_video = video.set_audio(audio)
    final_video.write_videofile('final_output_video.mp4', codec='libx264', audio_codec='aac')
    
    print('Saved output video to:', filename)
