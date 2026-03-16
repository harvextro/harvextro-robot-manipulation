import cv2

LEFT_INDEX = 1
RIGHT_INDEX = 2

camL = cv2.VideoCapture(LEFT_INDEX)
camR = cv2.VideoCapture(RIGHT_INDEX)

count = 0

print("Press SPACE to capture image pair")
print("Press Q to quit")

while True:
    retL, frameL = camL.read()
    retR, frameR = camR.read()

    if not retL or not retR:
        break

    combined = cv2.hconcat([frameL, frameR])
    cv2.imshow("Stereo Capture", combined)

    key = cv2.waitKey(1)

    if key == ord(' '):
        cv2.imwrite(f"left_{count}.png", frameL)
        cv2.imwrite(f"right_{count}.png", frameR)
        print(f"Saved pair {count}")
        count += 1

    elif key == ord('q'):
        break

camL.release()
camR.release()
cv2.destroyAllWindows()