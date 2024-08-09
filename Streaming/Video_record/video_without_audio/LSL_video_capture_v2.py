# -*- coding: utf-8 -*-
"""
File: LSL_video_capture_v2.py
Author: Kieran Nichols (knichols4@wisc.edu)
Date: 8/5/24
Description: This script captures video from a webcam and streams it on LSL.
"""

def createOutlet(stream_name, channel_names, videoFile):
    import uuid
    import os
    import sys
    from pylsl import StreamInfo, StreamOutlet
    
    info = StreamInfo(name=stream_name,
                      type='StringStream',
                      channel_format='string',
                      channel_count=len(channel_names),
                      source_id=str(uuid.uuid4()))

    dir_file = os.path.dirname(filename)
    if not os.path.exists(dir_file):
        print('Creating folder', dir_file)
        os.makedirs(dir_file)
    if sys.platform == "linux":
        videoFile = os.path.splitext(filename)[0]+'.ogv'
  
    # Optionally, you can set channel names in the description
    chns = info.desc().append_child("channels")
    for name in channel_names:
        chn = chns.append_child("channel")
        chn.append_child_value("label", name)
        
    videoFile = filename
    info.desc().append_child_value("videoFile", videoFile)
    return StreamOutlet(info)


if __name__ == "__main__":
    import cv2
    from datetime import datetime
    import os 
    import time
    import numpy as np
    
    dir_out = os.path.dirname(os.path.realpath(__file__))
    # ## Use check_available_ports.py to find out the index number of the webcam/camera
    dev = 1
    new_fps = int(30)
    cap = cv2.VideoCapture(dev)
    if not cap.isOpened():
        print("Cannot open camera")
        import sys
        sys.exit()
    ret, frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    factor = 1
    adj_height, adj_width = int(2160), int(3840)#factor*int(height), factor*int(width)
    # adj_height, adj_width = int(720), int(1240)
    # adj_height =  int(factor*480) # int(720) # 
    # adj_width, adj_height = factor*int(height), factor*int(width)
    print('(fps, width, height) = ', (fps, width, height))
    print('(adj_width, adj_height) = ', (adj_width, adj_height))

    # https://stackoverflow.com/questions/48327616/logitech-brio-opencv-capture-settings
    # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    fourcc = cv2.VideoWriter_fourcc(*'M','J','P','G')    
    cap = cv2.VideoCapture()
    cap.open(dev, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FOURCC, fourcc) 
    cap.set(cv2.CAP_PROP_FPS, new_fps) #fps
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, adj_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, adj_height)
    
    str_datetime = datetime.now().strftime("_%Y%m%d_%H%M")
    filename = os.path.join(dir_out, 'Camera' + str(dev) +
                            str_datetime + '.avi') #avi mp4v 
    out = cv2.VideoWriter(filename, fourcc, new_fps, (adj_width, adj_height)) # original output video too fast
    frameCounter = 1
    outlet = createOutlet('video_data', ['frame_num', 'time in ms'], filename)
    
    # Start time
    old_time = time.perf_counter()
    start_time = time.time()
    diff, waiting, avg_time, diff_mean = 0.001, 0, 0, 0.1
    time_arr, diff_arr = [], []
    curr_time = time.perf_counter()
    elapsed_time_str = ''
    err = 0
    prev_err = 0
    prev_int = 0
    timestep = 0
    extra = 0
    next_time = time.perf_counter()
    
    interval = float(1/new_fps)
    sleep_time = interval
    resize_factor = 4
    
    while True:
            ret, frame = cap.read(cv2.CAP_DSHOW)
        # if ret == True:  
            # resize = cv2.resize(frame, (1024, 768))
            resize = cv2.resize(frame, (int(adj_width/resize_factor), int(adj_height/resize_factor)))
            elapsed_time1 = time.time() - start_time
            
            # # Put elapsed time text on the frame; Convert values to strings with desired formatting
            elapsed_time_str = f"{elapsed_time1:.5g} s"  # 5 significant figures
            diff_mean_str = f"{1/sleep_time:.5g} Hz"  # Assuming you want 1/diff_mean as frequency        
            text_to_display = f"Time: {elapsed_time_str}, Samp Freq: {diff_mean_str}, Frame Num: {frameCounter}"        
            cv2.putText(frame, text_to_display, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(resize, text_to_display, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            cv2.imshow('Press q to end.', resize) #frame   
        
            out.write(frame) # or frame for 4K
        
            outlet.push_sample([str(frameCounter), elapsed_time_str])
            frameCounter += 1
        
            if cv2.waitKey(1) == ord('q'):
                break        
        
            len_time = 10
            if len (time_arr) >= len_time:
                diff_arr = diff_arr[-len_time:] + [1/diff]
            diff_arr = diff_arr + [1/diff]
            diff_mean = np.nanmean(diff_arr)
        
            curr_time = time.perf_counter()
            diff = curr_time - old_time
            old_time = curr_time  
            
            if frameCounter == 2: 
                next_time = time.perf_counter()
                
            next_time += interval
            sleep_time = next_time - time.perf_counter()
            if sleep_time>0:
                time.sleep(sleep_time)
                
            Kp = 1; Ki = 0.1
            timestep = 1/float(new_fps)
            # err = diff
            err = timestep - diff #- extra
            prop_term = Kp * err
            int_term = prev_int + err*timestep
            waiting = prop_term + Ki*int_term
            prev_int = int_term
            
            print(sleep_time, waiting, frameCounter)

    # When everything done, release the capture    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print('Saved output video to:', filename)
    # filename is logged in 'info' -> 'desc' part of the xdf file saved by LSL Lab Recorder. 
    