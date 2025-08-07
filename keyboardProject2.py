from pynput.keyboard import Controller, Key
from collections import deque
import cv2
import mediapipe as mp

keyboard = Controller()

# === Finalized Key Maps ===
set_key_map = {
    1: list("ABCDEFGHIJKLMNOP"),
    2: list("QRSTUVWXYZ") + ['`', Key.tab, '-', '=', '[', ']'],
    3: list("0123456789") + ['\\', ';', "'", ',', '.', '/'],
    4: [Key.f1, Key.f2, Key.f3, Key.f4, Key.f5, Key.f6,
        Key.f7, Key.f8, Key.f9, Key.f10, Key.f11, Key.f12,
        Key.up, Key.down, Key.left, Key.right],
    5: [Key.print_screen, Key.scroll_lock, Key.pause,
        Key.insert, Key.home, Key.page_up, Key.page_down,
        Key.end, Key.esc, Key.caps_lock, Key.cmd],
    6: [Key.shift, Key.ctrl, Key.alt, Key.alt_gr, Key.cmd, Key.cmd]
}

KEY_TO_STRING_MAP = {
    Key.shift: "shift", Key.ctrl: "ctrl", Key.alt: "alt", Key.alt_gr: "alt_gr",
    Key.cmd: "cmd", Key.caps_lock: "caps_lock", Key.backspace: "backspace",
    Key.delete: "delete", Key.space: "space", Key.enter: "enter"
}

atomic_map = {
    7: Key.backspace, 8: Key.delete, 9: Key.space, 10: Key.enter
}

FINGER_TIPS = [4, 8, 12, 16, 20]
FINGER_PIPS = [2, 6, 10, 14, 18]
FINGER_NAMES = ['thumb', 'index', 'middle', 'ring', 'pinky']

# === Gesture Map ===
FINGER_COMBO_MAP = {
    ('left', frozenset({'ring', 'pinky', 'thumb'})): -1,
    ('right', frozenset({'thumb', 'index', 'middle'})): 1,
    ('right', frozenset({'thumb', 'index'})): 2,
    ('left', frozenset({'thumb', 'index', 'middle'})): 3,
    ('left', frozenset({'thumb', 'index'})): 4,
    ('right', frozenset({'thumb', 'pinky'})): 5,
    ('left', frozenset({'thumb', 'pinky'})): 6,
    ('right', frozenset({'index','pinky'})): 7,
    ('right', frozenset({'thumb', 'index', 'pinky'})): 8,
    ('left', frozenset({'index','pinky'})): 9,
    ('left', frozenset({'thumb', 'index', 'pinky'})): 10,
    ('right', frozenset({'index', 'middle','pinky'})): 11,
    ('right', frozenset({'index', 'middle'})): 12,
    ('right', frozenset({'index', 'middle', 'ring'})): 13,
    ('right', frozenset({'index', 'middle', 'ring', 'pinky'})): 14,
    ('right', frozenset({'thumb', 'index', 'middle', 'ring', 'pinky'})): 15,
    ('left', frozenset({'index', 'middle','pinky'})): 16,
    ('left', frozenset({'index', 'middle'})): 17,
    ('left', frozenset({'index', 'middle', 'ring'})): 18,
    ('left', frozenset({'index', 'middle', 'ring', 'pinky'})): 19,
    ('left', frozenset({'thumb', 'index', 'middle', 'ring', 'pinky'})): 20,
    ('right', frozenset({'middle', 'ring'})): 21,
    ('right', frozenset({'ring', 'pinky'})): 22,
    ('right', frozenset({'middle', 'ring', 'pinky'})): 23,
    ('left', frozenset({'middle', 'ring'})): 24,
    ('left', frozenset({'ring', 'pinky'})): 25,
    ('left', frozenset({'middle', 'ring', 'pinky'})): 26,
    ('right', frozenset({'thumb', 'ring', 'pinky'})): 27,
    ('right+left', frozenset({'right_thumb', 'right_index', 'left_thumb', 'left_index'})): 28,
    ('right+left', frozenset({'right_index', 'left_index'})): 29,
    ('right+left', frozenset({'right_pinky', 'left_pinky'})): 30,
}

# === State Variables ===
pressed = deque()
last_pressed = -2
active_set = -1
caps_lock_active = False

# === Setup MediaPipe Hands ===
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# === Main Loop ===
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    open_fingers_combined = set()
    handed_sets = {}

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[idx].classification[0].label.lower()
            landmarks = hand_landmarks.landmark
            open_fingers = []

            if handedness == 'right':
                if landmarks[FINGER_TIPS[0]].x < landmarks[FINGER_PIPS[0]].x:
                    open_fingers.append('thumb')
            else:
                if landmarks[FINGER_TIPS[0]].x > landmarks[FINGER_PIPS[0]].x:
                    open_fingers.append('thumb')

            for i in range(1, 5):
                if landmarks[FINGER_TIPS[i]].y < landmarks[FINGER_PIPS[i]].y:
                    open_fingers.append(FINGER_NAMES[i])

            handed_sets[handedness] = frozenset(open_fingers)
            open_fingers_combined |= {f"{handedness}_{f}" for f in open_fingers}

            mp.solutions.drawing_utils.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if len(handed_sets) == 2:
            combo = ('right+left', frozenset(open_fingers_combined))
        elif 'right' in handed_sets:
            combo = ('right', handed_sets['right'])
        elif 'left' in handed_sets:
            combo = ('left', handed_sets['left'])
        else:
            combo = None

        output = FINGER_COMBO_MAP.get(combo, 0)
    else:
        output = 0
        combo = None

    debug = f"nowPressed={output}\nactiveSet={active_set}\nlast_pressed={last_pressed}\npressed={[KEY_TO_STRING_MAP.get(k, str(k)) for k in pressed]}\nfrozenset={open_fingers_combined}\ncaps_lock_active={caps_lock_active}\ncombo={combo}"
    for i, line in enumerate(debug.split('\n')):
        cv2.putText(image, line, (10, image.shape[0] - 140 + 20 * i),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Gesture Control", image)

    nowPressed = output

    if last_pressed == nowPressed:
        pass

    elif nowPressed == -1:
        while pressed:
            keyboard.release(pressed.pop())
        active_set = -1
        last_pressed = nowPressed

    elif nowPressed == 0:
        pass

    elif 1 <= nowPressed <= 6:
        active_set = nowPressed

    elif 7 <= nowPressed <= 10:
        key = atomic_map[nowPressed]
        keyboard.press(key)
        keyboard.release(key)

    elif nowPressed == 27:
        keyboard.press(Key.ctrl)
        keyboard.press('z')
        keyboard.release('z')
        keyboard.release(Key.ctrl)

    elif nowPressed == 28:
        keyboard.press(Key.ctrl)
        keyboard.press('a')
        keyboard.release('a')
        keyboard.release(Key.ctrl)

    elif nowPressed == 29:
        keyboard.press(Key.ctrl)
        keyboard.press('c')
        keyboard.release('c')
        keyboard.release(Key.ctrl)

    elif nowPressed == 30:
        keyboard.press(Key.ctrl)
        keyboard.press('v')
        keyboard.release('v')
        keyboard.release(Key.ctrl)

    elif 11 <= nowPressed <= 26:
        idx = nowPressed - 11
        if active_set in set_key_map and idx < len(set_key_map[active_set]):
            key = set_key_map[active_set][idx]

            if key == Key.caps_lock:
                caps_lock_active = not caps_lock_active
                keyboard.press(key)
                keyboard.release(key)
                last_pressed = nowPressed
                continue

            if active_set == 6:
                if key not in pressed:
                    keyboard.press(key)
                    pressed.append(key)
            else:
                if isinstance(key, str) and len(key) == 1:
                    key_to_type = key.upper() if caps_lock_active else key.lower()
                    keyboard.press(key_to_type)
                    keyboard.release(key_to_type)
                else:
                    keyboard.press(key)
                    keyboard.release(key)

                while pressed:
                    keyboard.release(pressed.pop())

    last_pressed = nowPressed

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
