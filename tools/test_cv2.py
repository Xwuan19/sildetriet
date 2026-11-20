# -*- coding: utf-8 -*-
try:
    import cv2
    print("cv2 available")
    cap = cv2.VideoCapture("preview_red/test_3d_morph.mp4")
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("preview_red/test_3d_f0.jpg", frame)
        print("Frame 0 saved!")
    cap.release()
except Exception as e:
    print("Error:", e)
