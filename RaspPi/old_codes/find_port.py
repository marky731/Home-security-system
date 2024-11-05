import cv2

for i in range(0, 32):  # Adjust the range as necessary
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera found at /dev/video{i}")
        ret, frame = cap.read()
        if ret:
            cv2.imshow(f'Frame from /dev/video{i}', frame)
            cv2.waitKey(0)
        else:
            print("not ret: ", i)
        cap.release()
    else:
        print(f"No camera found at /dev/video{i}")
cv2.destroyAllWindows()
