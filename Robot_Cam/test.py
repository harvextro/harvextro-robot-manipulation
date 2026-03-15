'''import cv2

for i in range(5):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if cap.isOpened():
        print(f"Opening camera index {i}")
        ret, frame = cap.read()
        if ret:
            cv2.imshow(f"Camera {i}", frame)
            cv2.waitKey(3000)  # show for 3 seconds
        cap.release()
        cv2.destroyAllWindows()'''

'''import cv2

camL = cv2.VideoCapture(1)
camR = cv2.VideoCapture(2)

while True:
    retL, frameL = camL.read()
    retR, frameR = camR.read()

    if retL and retR:
        cv2.imshow("Left Camera", frameL)
        cv2.imshow("Right Camera", frameR)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camL.release()
camR.release()
cv2.destroyAllWindows()'''

import cv2
import numpy as np

LEFT_INDEX = 1
RIGHT_INDEX = 2

camL = cv2.VideoCapture(LEFT_INDEX)
camR = cv2.VideoCapture(RIGHT_INDEX)

# Force resolution
WIDTH = 640
HEIGHT = 480

for cam in [camL, camR]:
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

stereo = cv2.StereoBM_create(numDisparities=16*5, blockSize=15)

print("Press 'q' to quit")

while True:
    retL, frameL = camL.read()
    retR, frameR = camR.read()

    if not retL or not retR:
        break

    grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)

    disparity = stereo.compute(grayL, grayR)

    # Normalize for display
    disp_norm = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
    disp_norm = np.uint8(disp_norm)

    cv2.imshow("Left", frameL)
    cv2.imshow("Right", frameR)
    cv2.imshow("Depth Map", disp_norm)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camL.release()
camR.release()
cv2.destroyAllWindows()


