import cv2
import mediapipe as mp
import pyautogui
import platform
import pygetwindow as gw
import time
import os

def press_copy():
    os_name = platform.system()
    if os_name == "Darwin":  
        pyautogui.hotkey("command", "c")
    else: 
        pyautogui.hotkey("ctrl", "c")

def press_paste():
    os_name = platform.system()
    if os_name == "Darwin":
        pyautogui.hotkey("command", "v")
    else:
        pyautogui.hotkey("ctrl", "v")

MODEL_PATH = "gesture_recognizer.task"

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE,
    result_callback=None
)

recognizer = GestureRecognizer.create_from_options(options)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 200)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)


if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Starting gesture recognition. Press 'q' to exit.")

last_valid_gesture = None

frame_skip = 2 
frame_count = 0
dragging_window = False
active_window = None
last_hand_pos = (0, 0)

while True:
    frame_count += 1
    if frame_count % frame_skip != 0:
        continue
    
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    result = recognizer.recognize(mp_image)

    current_gesture = None
    if result.gestures:
        gesture = result.gestures[0][0]
        current_gesture = gesture.category_name.strip().lower()
        score = gesture.score

        current_norm = current_gesture if current_gesture else None
        last_norm = last_valid_gesture if last_valid_gesture else None

        if current_norm in ("open_palm", "closed_fist"):
            if last_norm is not None and last_norm in ("open_palm", "closed_fist") and current_norm != last_norm:
                #print(f"Checking transition from '{last_norm}' to '{current_norm}'")
                if last_norm == "open_palm" and current_norm == "closed_fist":
                    print("Copy action triggered!")
                    press_copy()
                elif last_norm == "closed_fist" and current_norm == "open_palm":
                    print("Paste action triggered!")
                    press_paste()
            last_valid_gesture = current_gesture

        # pointing_up
        elif current_norm == "pointing_up":
            landmarks = result.hand_landmarks[0] 
            x = int(landmarks[0].x * frame.shape[1])
            y = int(landmarks[0].y * frame.shape[0])

            if not dragging_window:
                win = gw.getActiveWindow()
                if win:
                    dragging_window = True
                    last_hand_pos = (x, y)
                    active_window = win
            else:
                dx = x - last_hand_pos[0]
                dy = y - last_hand_pos[1]

                dead_zone = 3
                if abs(dx) < dead_zone and abs(dy) < dead_zone:
                    pass
                else:
                    speed_multiplier = 3
                    dx_fast = int(dx * speed_multiplier)
                    dy_fast = int(dy * speed_multiplier)

                    max_move = 40
                    dx_fast = max(-max_move, min(dx_fast, max_move))
                    dy_fast = max(-max_move, min(dy_fast, max_move))

                    if active_window:
                        try:
                            active_window.moveTo(active_window.left + dx_fast, active_window.top + dy_fast)
                        except Exception as e:
                            print("Error moving window:", e)
                            dragging_window = False  
                    last_hand_pos = (x, y)

        else:
            dragging_window = False

    cv2.imshow("Saturday 1.0", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()