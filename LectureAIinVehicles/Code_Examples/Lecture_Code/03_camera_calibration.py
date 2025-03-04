import numpy as np
import cv2
import glob


print("\n\n\n############################################################")
print("Welcome to the Artificial Intelligence Lecture 2: Perception")
print("############################################################ \n")

print("\n **** Codeexample 3: Camera Calibration  *** \n")

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


print("Show Camera images ")
# Load all the images from the camera_calibration folder
images = glob.glob('Camera_Calibration/*.jpg')

img = cv2.imread('Camera_Calibration/image_1.jpg')
cv2.imshow('img',img)
cv2.waitKey(500)
input("Press Any key for further action....\n")

# Calculcate the cornes of different pictures and add the corner points to an array
for fname in images:
    print("Draw and display the corners")
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(500)
        input("Press Any key for further action....\n")

cv2.destroyAllWindows()

# With the corners we now calculate the camera matrix, distortion coefficients, rotation and translation vectors etc.
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

# With this parameters we can now undistort any image we want
print("Undistort the image")
img = cv2.imread('Camera_Calibration/image_3.jpg')
h,  w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# Display the undistorted picture
print("Show undistorted image")
cv2.imshow('Undistorted Image',dst)
cv2.waitKey(500)
input("Press Any key for further action....\n")

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('Camera_Calibration/calibresult.png',dst)
