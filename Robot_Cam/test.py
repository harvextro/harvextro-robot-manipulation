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

import cv2

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
cv2.destroyAllWindows()

