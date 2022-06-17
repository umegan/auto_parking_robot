import cv2 as cv
import sys
import numpy as np


def main():
    videoCapture = cv.VideoCapture(0)
    prewCircle = None
    dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2 
    
    while True:
        ret, frame = videoCapture.read()
        if not ret: break

        original = frame.copy()
        hvsFrame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        lower = np.array([0, 0, 0], dtype="uint8")
        upper = np.array([328, 57, 93], dtype="uint8")
        mask = cv.inRange(hvsFrame, lower, upper)
        # blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)


        rows = mask.shape[0]
        circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 1, rows /5,
                            param1= 100, param2=30,
                            minRadius=50, maxRadius=0)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            chosen = None
            for i in circles[0, :]:
                if chosen is None: chosen = i
                if prewCircle is not None:
                    if dist(chosen[0], chosen[1], prewCircle[0], prewCircle[1]) <= dist(i[0], i[1], prewCircle[0], prewCircle[1]):
                        chosen = i
                cv.circle(frame, (chosen[0], chosen[1]), 1, (0, 100, 100), 3)
                cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (255, 0, 255), 3)
                prewCircle  = chosen
                print("x, y= ", i[0], ",", i[1])


        cv.imshow("detected circles", frame)
        if cv.waitKey(1) % 0xFF == ord("q"): break

    videoCapture.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
    