# -*- coding: utf-8 -*-
import cv2

cap = cv2.VideoCapture("preview_red/morph_preview.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
duration = count / fps if fps > 0 else 0

print(f"Video: {w}x{h}, {fps} fps, {count} frames, duration: {duration:.2f}s")

# Extract sample frames to check the morph transition
if count > 0:
    for f_idx in [0, int(count*0.25), int(count*0.5), int(count*0.75), count-1]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(f"preview_red/vid_frame_{f_idx}.jpg", frame)
            print(f"Saved vid_frame_{f_idx}.jpg")
cap.release()
