import cv2
import numpy as np
import glob
import os

# -----------------------------
# SETTINGS
# -----------------------------
chessboard_size = (8, 5)      # inner corners (IMPORTANT)
square_size = 3.5             # in cm (change to 0.035 if using meters)

# -----------------------------
# TERMINATION CRITERIA
# -----------------------------
criteria = (cv2.TERM_CRITERIA_EPS + 
            cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# -----------------------------
# PREPARE OBJECT POINTS
# -----------------------------
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0],
                       0:chessboard_size[1]].T.reshape(-1, 2)
objp = objp * square_size

objpoints = []
imgpointsL = []
imgpointsR = []

# -----------------------------
# LOAD IMAGES
# -----------------------------
left_images = sorted(glob.glob("left_*.png"))
right_images = sorted(glob.glob("right_*.png"))

print("Left images:", len(left_images))
print("Right images:", len(right_images))

if len(left_images) == 0:
    print("❌ No images found. Check filename pattern.")
    exit()

# -----------------------------
# FIND CHESSBOARD CORNERS
# -----------------------------
for imgL_path, imgR_path in zip(left_images, right_images):

    imgL = cv2.imread(imgL_path)
    imgR = cv2.imread(imgR_path)

    grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    # More robust detector
    retL, cornersL = cv2.findChessboardCornersSB(grayL, chessboard_size)
    retR, cornersR = cv2.findChessboardCornersSB(grayR, chessboard_size)

    print("Detected:", retL, retR)

    if retL and retR:
        objpoints.append(objp)
        imgpointsL.append(cornersL)
        imgpointsR.append(cornersR)

        # Draw corners (for visual debug)
        cv2.drawChessboardCorners(imgL, chessboard_size, cornersL, retL)
        cv2.drawChessboardCorners(imgR, chessboard_size, cornersR, retR)

        cv2.imshow("Left", imgL)
        cv2.imshow("Right", imgR)
        cv2.waitKey(500)

cv2.destroyAllWindows()

print("Total valid pairs:", len(objpoints))

if len(objpoints) == 0:
    print("❌ No valid pairs detected. Fix chessboard or size.")
    exit()

# -----------------------------
# CALIBRATE EACH CAMERA
# -----------------------------
retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(
    objpoints, imgpointsL, grayL.shape[::-1], None, None)

retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(
    objpoints, imgpointsR, grayR.shape[::-1], None, None)

print("Left Camera Matrix:\n", mtxL)
print("Right Camera Matrix:\n", mtxR)

# -----------------------------
# STEREO CALIBRATION
# -----------------------------
flags = cv2.CALIB_FIX_INTRINSIC

retStereo, _, _, _, _, R, T, E, F = cv2.stereoCalibrate(
    objpoints,
    imgpointsL,
    imgpointsR,
    mtxL,
    distL,
    mtxR,
    distR,
    grayL.shape[::-1],
    criteria=criteria,
    flags=flags
)

print("Stereo Calibration RMS Error:", retStereo)
print("Rotation Matrix:\n", R)
print("Translation Vector:\n", T)

# -----------------------------
# SAVE CALIBRATION DATA
# -----------------------------
np.savez("stereo_calibration_data.npz",
         mtxL=mtxL,
         distL=distL,
         mtxR=mtxR,
         distR=distR,
         R=R,
         T=T)

print("✅ Calibration data saved as stereo_calibration_data.npz")