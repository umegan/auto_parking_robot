import cv2
import numpy as np
import matplotlib.pyplot as plt

def edge_detection(img, blur_ksize=5, threshold1=70, threshold2=200):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gaussian = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    img_canny = cv2.Canny(img_gaussian, threshold1, threshold2)

    return img_canny

img = cv2.imread('stack.png')
image = edge_detection(img)

minLineLength = 300
maxLineGap = 80
lines = cv2.HoughLinesP(image,1,np.pi/180,50,minLineLength,maxLineGap)

equations = []
for line in lines:
    x1,y1,x2,y2 = line[0]
    equations.append(np.cross([x1,y1,1],[x2,y2,1]))
    cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)

font = cv2.FONT_HERSHEY_SIMPLEX
thetas = []
N = len(equations)
for ii in range(1,N):
    a1,b1,c1 = equations[0]
    a2,b2,c2 = equations[ii]
    # intersection point
    pt = np.cross([a1,b1,c1],[a2,b2,c2])
    pt = np.int16(pt/pt[-1])
    # angle between two lines
    num = a1*b2 - b1*a2
    den = a1*a2 + b1*b2
    if den != 0:
        theta = abs(np.arctan(num/den))*180/3.1416
        # show angle and intersection point
        cv2.circle(img, (pt[0],pt[1]), 5, (255,0,0), -1)
        cv2.putText(img, str(round(theta, 1)), (pt[0]-20,pt[1]-20), font, 0.8, (255,0,0), 2, 0)
        thetas.append(theta)

plt.imshow(img)
plt.show()
