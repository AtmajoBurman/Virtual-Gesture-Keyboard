# Virtual Keyboard using Hand Gestures ✋⌨️

This project implements a **virtual keyboard** system using **Python**, **OpenCV**, and **MediaPipe**. It uses hand gesture detection to simulate keypresses by tracking fingers in real-time through a webcam.

## 📌 Features

- Real-time hand tracking using **MediaPipe Hands**
- Finger combination detection for virtual key input
- Customizable key mappings across multiple "sets" (like shift layers)
- Displays the detected key on screen
- Prints the pressed keys in the terminal
- Can be integrated with gesture-controlled systems

## 📷 Demo

> [Insert link to demo GIF or video here, if available]

## ⚙️ Requirements

- **Python**: Version **3.7 to 3.9** recommended (MediaPipe may not work well with Python ≥ 3.10)
- **Libraries**:
  - `opencv-python`
  - `mediapipe`

You can install the required dependencies using:

```bash
pip install opencv-python mediapipe
```

## 🗂️ Project Structure

```
virtual-keyboard/
├── main.py           # Main implementation file
├── README.md         # Project documentation
```

## 🚀 How to Run

1. Clone the repository:

```bash
git clone https://github.com/your-username/virtual-keyboard.git
cd virtual-keyboard
```

2. Install the dependencies:

```bash
pip install opencv-python mediapipe
```

3. Run the application:

```bash
python main.py
```

4. A window will open using your webcam. Show your hand, and the virtual keyboard will detect finger gestures and print corresponding characters.

## 🎯 Finger Mapping Logic

The code uses `frozenset` combinations of up fingers to detect which key to press. There are multiple sets of keys (like layers), and the active set is determined by which finger (e.g., thumb) is down.

You can configure or extend the `SET_KEY_MAP` dictionary and gesture detection logic to suit different languages, shortcuts, or use cases.

## ⚠️ Notes

- Use **Python < 3.10** for best compatibility with `mediapipe`
- Ensure your lighting and webcam quality is decent for accurate detection
- Avoid cluttered backgrounds to reduce noise in detection

## 🧠 Future Improvements

- Integration with system keyboard events (`pyautogui`)
- GUI-based virtual keyboard layout
- Sound or haptic feedback
- Multi-language or emoji support

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).

---

**Developed with ❤️ for gesture-based computing**

## 👤 Author

**Atmajo Burman**  
Logic Designer • Coder • Enthusiast
