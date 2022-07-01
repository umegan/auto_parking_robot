import cv2
from cv2 import circle
import numpy as np


def detect(video_path):
    """
    input: image

    ouput: circle x direction from input image
    """
    # 
    cap = cv2.VideoCapture(video_path)

    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")

    # Read until video is completed
    while(cap.isOpened()):
    # Capture frame-by-frame
        ret, img = cap.read()
        if ret == True:

            # Check if image is loaded fine
            hsvimage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            # Mask color
            lower = np.array([150, 10, 10], dtype="uint8")
            upper = np.array([180, 255, 255], dtype="uint8")
            mask = cv2.inRange(hsvimage, lower, upper)
            img1 = img.copy()
            img1[mask==0] = [0, 0, 0]

            hsv2rgb = cv2.cvtColor(img1, cv2.COLOR_HSV2RGB)
            gray = cv2.cvtColor(hsv2rgb, cv2.COLOR_RGB2GRAY)
            gray = cv2.medianBlur(gray, 5)

            rows = mask.shape[0]
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows,
                                    param1= 100, param2=19,
                                    minRadius=60, maxRadius=0)
        else:
            break
            

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv2.circle(img, center, 4, (0, 100, 100), 3)
                # circle center text
                cv2.putText(img, f"x= {str(i[0])}",center, cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 4, cv2.LINE_AA)
                # circle outline
                radius = i[2]
                cv2.circle(img, center, radius, (255, 0, 255), 3)
            # output: x direction
        # print(circles[0][0][0])

        # Show video
        cv2.imshow("detected circles", img)
        cv2.imshow("mask", gray)

        # Press "q" to quit 
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
   
    cap.release()

# Closes all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_path = 'datas/robot.mp4'
    detect(video_path)
    
    