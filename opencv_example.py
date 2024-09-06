# This program is the program I will be using to test the features of the OpenCV library
# https://www.youtube.com/watch?v=oXlwWbU8l2o


import cv2 as cv
import numpy as np
import time
import math
import typing

WIDTH = 500
HEIGHT = 500

# Linear Interpolation
def lerp(start: float, end: float, t: float) -> float:
    return start + t * (end - start)

# Returns the rescaled image/video
def resizeFrame(frame, width, height):
    return cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)

# Returns the grayscale version of the frame
def greyscaleFrame(frame):
    return cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

# Gaussian blur on frame
def blurFrame(frame, factor: int):
    return cv.GaussianBlur(frame, (factor, factor), cv.BORDER_DEFAULT)

# Canny edge detector
def edgeCascade(frame):
    return cv.Canny(frame, 125, 175)

# Dilates the frame
def dilateFrame(frame):
    return cv.dilate(frame, (15, 15), iterations = 2)

# Erodes  the frame
def erodeFrame(frame):
    return cv.erode(frame, (15, 15), iterations = 2)

# Translates the frame by x and y
def translateFrame(frame, x, y):
    transMat = np.float32([[1,0,x],[0,1,y]])
    dimensions = (frame.shape[1], frame.shape[0])
    return cv.warpAffine(frame, transMat, dimensions)

# Rotates the frame around rotationPoint theta degrees
def rotateFrame(frame, theta, rotationPoint = None):
    (height, width) = frame.shape[:2]

    if rotationPoint is None:
        rotationPoint = (width//2, height//2)

    rotMat = cv.getRotationMatrix2D(rotationPoint, theta, 1.0)
    dimensions = (width, height)

    return cv.warpAffine(frame, rotMat, dimensions)

# Flips the frames
def flipYFrame(frame):
    return cv.flip(frame, 0)

def flipXFrame(frame):
    return cv.flip(frame, 1)

def flipXYFrame(frame):
    return cv.flip(frame, -1)

#Crops the frame
def cropFrame(frame, coord1: Tuple[int, int], coord2: Tuple[int, int]):
    return frame[ coord1[0]:coord1[1] , coord2[0]:coord2[1] ]


# Draws shapes and text on the frame
def drawOnFrame(frame):
    cv.rectangle(frame, pt1 = (100,100), pt2 = (300,200), color = (240, 180, 180), thickness=cv.FILLED)
    cv.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 100, (180, 180, 240), thickness=cv.FILLED)
    cv.putText(frame, 'VOID', (100,200), cv.FONT_HERSHEY_TRIPLEX, 2, (0,0,0), thickness=3)

if __name__ == "__main__":
    
    # Creating a blank Canvas
    #
    # blank = np.zeros((WIDTH, HEIGHT, 3), dtype='uint8')
    # blank[:] = (180,250,180)

    # Start the timer
    startTime = time.time()

    # Camera
    capture = cv.VideoCapture(0)

    toggle = False
    while True:
        
        # Run the timer
        elapsed_time = time.time() - startTime

        # Frame returns the matrix of pixels from capture
        isTrue, initialFrame = capture.read() #capture.read() returns a tuple (isTrue: bool, frame: Mat)
        frame = initialFrame #flipXFrame(resizeFrame(initialFrame, WIDTH, HEIGHT))
        
        # Draws objects on the window
        #
        # drawOnFrame(frame)
        
        # Various effects
        #
        # if(toggle):
            # frame = greyscaleFrame(frame)
            # frame = blurFrame(frame, 3)
            # frame = edgeCascade(frame)
            # frame = dilateFrame(frame)
            # frame = erodeFrame(frame)
            # frame = translateFrame(frame, math.cos(elapsed_time) * 100, math.sin(elapsed_time) * 100)
            # frame = rotateFrame(frame, elapsed_time * 180 / math.pi)
            # frame


        # Displays the frame in a window called 'Video'
        cv.imshow('Video', frame)
        # cv.imshow('Blank', blank);

        # Press d to exit
        if cv.waitKey(20) &  0xFF==ord('d'):
            break

        if cv.waitKey(20) &  0xFF==ord('f'):
            toggle = not toggle
    
    capture.release()
    cv.destroyAllWindows()
