import cv2
import numpy as np
import time

# -----------------------------
# LOAD CALIBRATION DATA
# -----------------------------
data = np.load("stereo_calibration_data.npz")

mtxL = data['mtxL']
distL = data['distL']
mtxR = data['mtxR']
distR = data['distR']
R = data['R']
T = data['T']

# -----------------------------
# OPEN CAMERAS (DEFAULT BACKEND)
# -----------------------------
capL = cv2.VideoCapture(1)
capR = cv2.VideoCapture(2)

# Set resolution
capL.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capL.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
capR.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capR.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not capL.isOpened():
    print("❌ Left camera failed to open")
    exit()

if not capR.isOpened():
    print("❌ Right camera failed to open")
    exit()

# Warm up cameras (IMPORTANT for MSMF)
time.sleep(2)

retL, frameL = capL.read()
retR, frameR = capR.read()

if not retL or frameL is None:
    print("❌ Left camera not giving frames")
    exit()

if not retR or frameR is None:
    print("❌ Right camera not giving frames")
    exit()

h, w = frameL.shape[:2]

# -----------------------------
# STEREO RECTIFICATION
# -----------------------------
R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
    mtxL, distL,
    mtxR, distR,
    (w, h),
    R, T
)

mapLx, mapLy = cv2.initUndistortRectifyMap(
    mtxL, distL, R1, P1, (w, h), cv2.CV_32FC1)

mapRx, mapRy = cv2.initUndistortRectifyMap(
    mtxR, distR, R2, P2, (w, h), cv2.CV_32FC1)

# -----------------------------
# STEREO MATCHER
# -----------------------------
stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=16*8,
    blockSize=5,
    P1=8 * 3 * 5**2,
    P2=32 * 3 * 5**2,
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32
)

print("✅ Stereo running. Press 'q' to quit")

depth_value = 0

def mouse_callback(event, x, y, flags, param):
    global depth_value, disparity, Q
    if event == cv2.EVENT_LBUTTONDOWN:
        points_3D = cv2.reprojectImageTo3D(disparity, Q)
        depth_value = points_3D[y, x][2]
        print(f"Depth at ({x},{y}) = {depth_value:.2f} cm")

cv2.namedWindow("Left Rectified")
cv2.setMouseCallback("Left Rectified", mouse_callback)

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    retL, frameL = capL.read()
    retR, frameR = capR.read()

    if not retL or not retR:
        print("⚠ Frame grab failed")
        continue

    rectL = cv2.remap(frameL, mapLx, mapLy, cv2.INTER_LINEAR)
    rectR = cv2.remap(frameR, mapRx, mapRy, cv2.INTER_LINEAR)

    grayL = cv2.cvtColor(rectL, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(rectR, cv2.COLOR_BGR2GRAY)

    disparity = stereo.compute(grayL, grayR).astype(np.float32) / 16.0

    disp_display = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
    disp_display = np.uint8(disp_display)

    cv2.putText(rectL,
                f"Depth: {depth_value:.2f} cm",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2)

    cv2.imshow("Left Rectified", rectL)
    cv2.imshow("Disparity", disp_display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capL.release()
capR.release()
cv2.destroyAllWindows()