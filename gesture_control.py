import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

# Function to count fingers
def count_fingers(hand_landmarks):
    tips = [8, 12, 16, 20]
    count = 0
    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        count += 1
    # Other fingers
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1
    return count

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    finger_count = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            finger_count = count_fingers(hand_landmarks)

    # Gesture logic
    if finger_count == 1:
        pyautogui.keyDown('up')
        pyautogui.keyUp('down')
        print("Accelerating")
    elif finger_count == 2:
        pyautogui.keyDown('down')
        pyautogui.keyUp('up')
        print("Braking")
    else:
        pyautogui.keyUp('up')
        pyautogui.keyUp('down')
        print("Idle")

    # Display
    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
