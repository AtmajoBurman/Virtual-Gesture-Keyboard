# Virtual Keyboard using Hand Gestures ✋⌨️

This project implements a **virtual keyboard** system using **Python**, **OpenCV**, and **MediaPipe**. It uses hand gesture detection to simulate keypresses by tracking fingers in real-time through a webcam.

---

## 📌 Features

- Real-time hand tracking using **MediaPipe Hands**
- Finger combination detection for virtual key input
- Customizable key mappings across multiple "sets" (like shift layers)
- Displays the detected key on screen
- Prints the pressed keys in the terminal
- Can be integrated with gesture-controlled systems

---

## 📷 Demo

> [Insert link to demo GIF or video here, if available]

---

## ⚙️ Requirements

- **Python**: Version **3.7 to 3.9** recommended  
  *(MediaPipe may not work well with Python ≥ 3.10)*
- **Libraries**:
  - `opencv-python`
  - `mediapipe`

Install the dependencies:

```bash
pip install opencv-python mediapipe
```

---

## 🗂️ Project Structure

```
virtual-keyboard/
├── keyboardProject2.py   # Main implementation file
├── README.md             # Project documentation
├── FINGER_FLOW3.pdf      # Guides finger combinations to mapped numbers
├── INDEX_FLOW3.pdf       # Maps numbers (from finger combos) to keys
```

---

## 🚀 How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/virtual-keyboard.git
   cd virtual-keyboard
   ```

2. **Install the dependencies**:
   ```bash
   pip install opencv-python mediapipe
   ```

3. **Run the application**:
   ```bash
   python keyboardProject2.py
   ```

4. A webcam window will open. Show your hand, and the virtual keyboard will detect finger gestures and print corresponding characters.

---

## 🧾 How to Use: Finger Combinations and Key Mappings

The system detects a specific **combination of up fingers**, forms a **frozenset**, and maps it to a number.

- This number identifies a **key** from the active key-set.
- To **understand what gesture corresponds to what key**, refer to the following two PDFs:

### 📘 `FINGER_FLOW3.pdf`
- Explains which **finger combination** maps to which **gesture number**.
- Each gesture combination (like thumb + index, or index + ring) is assigned a unique number.

### 📙 `INDEX_FLOW3.pdf`
- Shows how each **gesture number** maps to a **keyboard character**, based on the current set (layer).

> 🧠 **IMPORTANT**: Keep both PDFs open side-by-side while using the application, as they work together to guide you.

---

## 🎯 Finger Mapping Logic

The logic uses a dictionary like:

```python
SET_KEY_MAP = {
    1: [...],  # First set of keys
    2: [...],  # Second set, like Shift layer
    ...
}
```

- Each combination of up fingers (converted to a frozenset) gives an index.
- The set (layer) is dynamically selected based on which fingers are down (like thumb for Set 1, pinky for Set 2).
- The number derived from the finger combination is then used to access a key from the current active set.

You can edit `SET_KEY_MAP` in `keyboardProject2.py` to add new keys or change mappings.

---

## ⚠️ Notes

- Use **Python < 3.10** for best compatibility with `mediapipe`
- Ensure good lighting and camera positioning for reliable detection
- Avoid busy or cluttered backgrounds to reduce false detection
- Keep the **FINGER_FLOW3.pdf** and **INDEX_FLOW3.pdf** open for reference

---

## 🧠 Future Improvements

- Integration with system keyboard events (`pyautogui`)
- GUI-based virtual keyboard layout
- Sound or haptic feedback
- Multi-language or emoji support

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).

---

**Developed with ❤️ for gesture-based computing**

## 👤 Author

**Atmajo Burman**  
Logic Designer • Coder • Enthusiast
