# Hand Tracking Module
import cv2
import mediapipe as mp
import time

class HandTracker():
    def __init__(self,image_mode=False, max_num_hands=2,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.image_mode = image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()

    # method to find hand landmarks
    def findHand(self, img, draw=True):
        RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self.hands.process(RGBimg)

        self.multiHandLandmarks = result.multi_hand_landmarks

        if self.multiHandLandmarks:
            for handLandmarks in self.multiHandLandmarks:
                if draw:
                    mp.solutions.drawing_utils.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)
        return img

    # method to working with each landmark
    def findPosition(self, img, handNo=0, draw=False):
        landmarkList = []  # [index, x, y]

        if self.multiHandLandmarks:
            myHand = self.multiHandLandmarks[handNo]

            for index, handLandmark in enumerate(myHand.landmark):
                h, w, c = img.shape  # returns height, width, center
                cx, cy = int(handLandmark.x * w), int(handLandmark.y * h)
                landmarkList.append([index, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        return landmarkList

def main():
    video = cv2.VideoCapture(0)
    # Object for the class HandTracker()
    handTraker = HandTracker()

    previousTime = 0
    currentTime = 0

    while True:
        success, img = video.read()

        img = handTraker.findHand(img)

        landmarkList = handTraker.findPosition(img, draw=True)
        if len(landmarkList) != 0:
            print(landmarkList)

        # Calculating frames per second
        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 13:
            exit()

if __name__ == "__main__":
    main()
