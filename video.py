#!/usr/bin/env python3


import time
import sys
import cv2
from color import name_to_bgr, detect_bgr, rect_average
import json
import threading
import color
import numpy as np

REGION_SIZE = 32
REGION_PAD = 192
PREVIEW_SIZE = 64
PREVIEW_PAD = 1
PREVIEW_CUBE_SIZE = (PREVIEW_SIZE+PREVIEW_PAD)*3
PREVIEW_X = 1020
PREVIEW_Y = 220
PREVIEW_SIDE_OFFSETS = [
    [PREVIEW_X+PREVIEW_CUBE_SIZE+20, PREVIEW_Y-PREVIEW_CUBE_SIZE-5],
    [PREVIEW_X, PREVIEW_Y],
    [PREVIEW_X+PREVIEW_CUBE_SIZE+5, PREVIEW_Y],
    [PREVIEW_X+PREVIEW_CUBE_SIZE*2+10, PREVIEW_Y],
    [PREVIEW_X+PREVIEW_CUBE_SIZE*3+15, PREVIEW_Y],
    [PREVIEW_X+PREVIEW_CUBE_SIZE+20, PREVIEW_Y+PREVIEW_CUBE_SIZE+5]
]

class Webcam:
    def __init__(self):
        self.update_state()
        print(PREVIEW_SIDE_OFFSETS)

    def draw_regions(self, frame):
        cv2.rectangle(frame, (960,0), (1920, 1080), (0, 0, 0), -1)
        for index in range(9):
            x, y = self.regions[index]
            rect  = frame[y:y+REGION_SIZE, x:x+REGION_SIZE]
            cv2.rectangle(frame, (x,y), (x+REGION_SIZE, y+REGION_SIZE), (255, 255, 255), 2)

            color = detect_bgr(rect_average(rect))[0]
            

    def draw_state(self, frame):
        for side in range(6):
            offsetx, offsety = PREVIEW_SIDE_OFFSETS[side]
            for y in range(3):
                for x in range(3):
                    color = self.state[side*9 + y*3 + x]
                    cv2.rectangle(frame,
                        (offsetx+x*(PREVIEW_SIZE+PREVIEW_PAD), offsety+y*(PREVIEW_SIZE+PREVIEW_PAD)),
                        (offsetx+x*(PREVIEW_SIZE+PREVIEW_PAD)+PREVIEW_SIZE, offsety+y*(PREVIEW_SIZE+PREVIEW_PAD)+PREVIEW_SIZE),
                        name_to_bgr(color), -1)

    def update_window(self, frame):
        self.draw_regions(frame)
        self.draw_state(frame)
        height, width, layers =  frame.shape
        resize = cv2.resize(frame, (width//2, height//2)) 
        cv2.imshow("win1", resize)


    def update_state(self, state = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"):
        self.state = state

    def video_loop(self):
        self.cam = cv2.VideoCapture(0)
        cv2.namedWindow("win1");
        cv2.moveWindow("win1", 20, 20);
        self.cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3) # auto mode
        # self.cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # manual mode
        # self.cam.set(cv2.CAP_PROP_EXPOSURE, 10)
        self.cam.set(cv2.CAP_PROP_AUTO_WB, 0)

        while self.running:
            ret, frame = self.cam.read()
   
            key = cv2.waitKeyEx(10)
            # print(key)
            if key == 27:
                break
            elif key == 63232:
                # print("Up arrow key was pressed")
                self.offset_y -= 5
                print("offset_y " + str(self.offset_y))
            elif key == 63233:
                # print("Down arrow key was pressed")
                self.offset_y += 5
                print("offset_y " + str(self.offset_y))
            elif key == 63235:
                # print("Right arrow key was pressed")
                self.offset_x += 5
                print("offset_x " + str(self.offset_x))
            elif key == 63234:
                # print("Left arrow key was pressed")
                self.offset_x -= 5
                print("offset_x " + str(self.offset_x))
            elif key == 45: # -
                self.zoom_factor /= 1.1
                print("zoom " + str(self.zoom_factor))
            elif key == 61: # +
                self.zoom_factor *= 1.1
                print("zoom " + str(self.zoom_factor))
            
            if ret:
                # Define the region of interest (ROI)
                height, width, _ = frame.shape
                halfWidth = int(width/2);
                x_center = int(width / 2) + self.offset_x
                y_center = int(height / 2) + self.offset_y

                roi_width = int(width // (2 * self.zoom_factor)) # by 2 because it's half the screen
                roi_height = int(height // (self.zoom_factor))

                # Get the interest area in the middle of the screen
                roi = cv2.getRectSubPix(frame, (roi_width, roi_height), (x_center, y_center))
                resized_roi = cv2.resize(roi, (halfWidth, height))
                
                # Fill array with zeros (same size as camera output), and put the image on the left
                self.current_frame = np.zeros((height, width, 3), dtype=np.uint8)
                self.current_frame[0:height, 0:halfWidth] = resized_roi
                self.update_window(self.current_frame)

        self.cam.release()
        cv2.destroyAllWindows()

    def start_video(self):
        # Offset and zoom set according to my camera
        # You can start from 0, 0, 1 and find the values that suit you
        self.offset_x = -75
        self.offset_y = 400
        self.zoom_factor = 2.5937424601000023

        self.running = True
        self.regions = []
        for y in range(3):
            for x in range(3):
                self.regions.append([220+x*(REGION_SIZE+REGION_PAD), 220+y*(REGION_SIZE+REGION_PAD)])
                
        self.video_loop()

    def stop_video(self):
        self.running = False

    def scan(self):
        state = []
        for index, (x,y) in enumerate(self.regions):
            rect  = self.current_frame[y:y+REGION_SIZE, x:x+REGION_SIZE]
            state.append(color.rect_average(rect))
        return state   

        return None

