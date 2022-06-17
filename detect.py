import cv2 as cv
import numpy as np


def main(src):
    """
    input: image

    ouput: circle x direction from input image
    """
    
    # Check if image is loaded fine
    hsvimage = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    lower = np.array([135, 0, 0], dtype="uint8")
    upper = np.array([175, 255, 255], dtype="uint8")
    mask = cv.inRange(hsvimage, lower, upper)
    
    
    rows = mask.shape[0]
    circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 1, rows /5,
                            param1= 100, param2=38,
                            minRadius=50, maxRadius=0)
    
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        # for i in circles[0, :]:
        #     center = (i[0], i[1])
            # circle center
            # cv.circle(src, center, 4, (0, 100, 100), 3)
            # cv.putText(src, f"x= {str(i[0])}",center, cv.FONT_HERSHEY_PLAIN, 4, (0, 100, 100), 5, cv.LINE_AA)
            # circle outline
            # radius = i[2]
            # cv.circle(src, center, radius, (255, 0, 255), 3)
        # output: x direction
        return circles[0][0][0]
    
    
    # cv.imshow("detected circles", src)
    # cv.imshow("mask", mask) 
    # cv.waitKey(0)


if __name__ == "__main__":
    img_path = 'datas/IMG_0381.jpg'

    # Loads an image
    src = cv.imread(cv.samples.findFile(img_path), cv.IMREAD_COLOR)
    print(main(src))
    