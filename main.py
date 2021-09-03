import cv2
import numpy
import time
import math
import handTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

tracker = htm.HandTracker(min_detection_confidence=0.85, min_tracking_confidence=0.85)

############################################################
# FROM GITHUB(https://github.com/AndreMiras/pycaw)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()

volRange = volume.GetVolumeRange()  # -74.0 to 0.0
minVol = volRange[0]  # -74.0
maxVol = volRange[1]  # 0.0

############################################################

previousTime = 0
currentTime = 0

video = cv2.VideoCapture(0)
video.set(3, 600)  # propId for width - 3
video.set(4, 300)  # propId for height - 4

while True:
    success, img = video.read()

    img = tracker.findHand(img)

    lmList = tracker.findPosition(img)
    if len(lmList) != 0:

        # getting landmarks of the tip of thumb and index fingers
        x1, y1 = lmList[4][1:3]
        x2, y2 = lmList[8][1:3]
        cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        # calculating length between tip of thumb and index fingers
        length = math.hypot((x2-x1), (y2-y1))  # 20 to 120
        # print(int(length))

        vol = numpy.interp(length, [20, 120], [minVol, maxVol])
        volBar = numpy.interp(length, [20, 120], [400, 150])
        volPercent = numpy.interp(length, [20, 120], [0, 100])

        volume.SetMasterVolumeLevel(vol, None)

        if length < 20:
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
        elif length > 120:
            cv2.circle(img, (cx, cy), 10, (245, 59, 223), cv2.FILLED)

        # Volume Bar
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 2)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f"{int(volPercent)}%", (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

    # Calculating frames per second
    currentTime = time.time()
    fps = int(1 / (currentTime-previousTime))
    previousTime = currentTime

    cv2.putText(img, f"FPS : {fps}", (40, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
    cv2.imshow("Gesture Control", img)
    key = cv2.waitKey(1)
    # Press "enter" to exit
    if key == 13:
        exit()
