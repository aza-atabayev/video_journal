import cv2
import threading
import datetime

from DAN.demo import get_prediction_video
import time
from pathlib import Path

class RecordingThread (threading.Thread):
    def __init__(self, name, camera, now):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        global file_path

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        Path(f"data/images/{now[0]}/").mkdir(parents=True, exist_ok=True)
        file_path = f'data/images/{now[0]}/{now[1]}.avi'
        self.out = cv2.VideoWriter(file_path,fourcc, 15.0, (1280,720))

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)

        self.out.release()
        get_prediction_video(file_path)

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()

class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(0)
        # Initialize video recording environment
        self.is_record = False
        self.out = None
        # Thread for recording
        self.recordingThread = None
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)

            # Record video
            # if self.is_record:
            #     if self.out == None:
            #         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            #         self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))
                
            #     ret, frame = self.cap.read()
            #     if ret:
            #         self.out.write(frame)
            # else:
            #     if self.out != None:
            #         self.out.release()
            #         self.out = None  

            return jpeg.tobytes()
      
        else:
            return None

    def start_record(self,now):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap, now)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()

            