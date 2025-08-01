import cv2
import mediapipe as mp
import pyautogui

# ===============================
# Initialize MediaPipe Hands
# ===============================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

# ===============================
# Function to count fingers
# ===============================
def count_fingers(hand_landmarks):
    """
    Count how many fingers are extended.
    Uses landmark positions to check if a finger is up or down.
    """
    tips = [8, 12, 16, 20]  # Finger tip landmark indexes
    count = 0

    # Thumb: check if it is open (comparing x-coordinates for left/right hand)
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        count += 1

    # Other fingers: check if tip is above PIP joint
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1

    return count

# ===============================
# Main Loop
# ===============================
while True:
    success, img = cap.read()
    if not success:
        print("❌ Could not access webcam.")
        break

    img = cv2.flip(img, 1)  # Mirror the image for natural interaction
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    finger_count = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            finger_count = count_fingers(hand_landmarks)

    # ===============================
    # Gesture Control Logic
    # ===============================
    if finger_count == 1:
        pyautogui.keyDown('up')
        pyautogui.keyUp('down')
        cv2.putText(img, "Accelerating 🚀", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    elif finger_count == 2:
        pyautogui.keyDown('down')
        pyautogui.keyUp('up')
        cv2.putText(img, "Braking 🛑", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    else:
        pyautogui.keyUp('up')
        pyautogui.keyUp('down')
        cv2.putText(img, "Idle 💤", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

    # ===============================
    # Display Window
    # ===============================
    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break

# ===============================
# Cleanup
# ===============================
cap.release()
cv2.destroyAllWindows()