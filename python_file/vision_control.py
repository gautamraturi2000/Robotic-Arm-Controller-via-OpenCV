import cv2
import mediapipe as mp
import serial

arduino = serial.Serial('COM5', 9600)  
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def map_value(value, from_min, from_max, to_min, to_max):
    return (value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min

def main():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                finger_landmarks = [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                                     hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]]

                for i, landmark in enumerate(finger_landmarks):
                    x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                    angle_deg = int(map_value(y, 0, frame.shape[0], 0, 180)) 
                    arduino.write(f"{i},{angle_deg}\n".encode())

                    cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (255, 0, 0), 2)

        cv2.imshow('Hand Gesture Control', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()

if __name__ == "__main__":
    main()
