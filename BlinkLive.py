# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import PySimpleGUI as sg
import time

def eye_aspect_ratio(eye):
   # calculate vertical distances
   vert_dist_1 = dist.euclidean(eye[1], eye[5])
   vert_dist_2 = dist.euclidean(eye[2], eye[4])

   #  calculate horizontal distances
   horiz_dist = dist.euclidean(eye[0], eye[3])

   ear = (vert_dist_1 + vert_dist_2) / (2 * horiz_dist)
   return ear


#  parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True, help="path to facial landmark predictor")
ap.add_argument("-v", "--video", type=str, default="", help="path to input video file")
args = vars(ap.parse_args())

#  threshold to determine if a blink occurred
EAR_THRESHOLD = 0.27
#  number of consecutive frames the threshold condition must be met
EAR_CONSECUTIVE_FRAMES = 4
#  counter for blinks
COUNTER = 0
#  total number of blinks
TOTAL = 0

layout = [ [sg.Text('Press OK to start the blink detection program')],
           [sg.OK(), sg.Cancel()] ]
# Create the Window