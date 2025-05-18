# AirGestures
AirGestures is a simple python project that uses MediaPipe and OpenCV to detect real-time hand gestures and translate them into desktop actions like copying, pasting, and dragging windows.

---
## 🎥 Demo

![AirGestures Demo](./demo.gif)

---
## Requirements
```txt
mediapipe==0.10.9
opencv-python
pyautogui
pygetwindow
```

---
## Install Dependencies
`
pip install mediapipe==0.10.9 opencv-python pyautogui pygetwindow
`

---
## System Requirements
- A working webcam (in-build or external)
- Python 3.8+

---
>#### NOTE
>###### For Dragging Windows
>- Windows: ✅ Fully supported
>- macOS: ⚠️ Drag may not work out-of-the-box due to strict windowing system
>- Linux: ⚠️ Requires X11-based environments; may not work reliably on Wayland
