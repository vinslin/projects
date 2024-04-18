import cv2
import mediapipe as mp
import math
import keyboard
import time

time.sleep(10)
# Function to control VLC with delay
def vlc_control(command):
    keyboard.press_and_release(command)  # Simulate keyboard press
    

# Initialize MediaPipe HandPose model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

# Define indices of the hand landmarks to calculate distance
point1_idx = 4 # Change this to the index of the first hand point
point2_idx = 8  # Change this to the index of the second hand point

def calculate_distance(hand_landmarks, point1_idx, point2_idx):
    # Get coordinates of the specified hand landmarks
    point1 = hand_landmarks.landmark[point1_idx]
    point2 = hand_landmarks.landmark[point2_idx]
    
    # Calculate Euclidean distance between the points
    distance = math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)
    #print(distance)
    return distance

# Open a video capture device (webcam)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
         break

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe HandPose model
    results = hands.process(frame_rgb)

    # Get hand landmarks if available
    if results.multi_hand_landmarks:
        # Extract first detected hand
        hand_landmarks = results.multi_hand_landmarks[0]

        # Draw landmarks on the frame
        for landmark in mp_hands.HandLandmark:
            landmark_point = hand_landmarks.landmark[landmark]
            x = int(landmark_point.x * frame.shape[1])
            y = int(landmark_point.y * frame.shape[0])
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        # Calculate distance between specified hand landmarks
        distance = [calculate_distance(hand_landmarks, 4, 8),calculate_distance(hand_landmarks, 4, 12),calculate_distance(hand_landmarks, 4, 16),calculate_distance(hand_landmarks, 4, 20),calculate_distance(hand_landmarks, 0, 20)]
        if (distance[0] < 0.07):
             vlc_control('ctrl+up')
             cv2.putText(frame, "VOLUME +5", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif (distance[1] < 0.08):
             vlc_control('ctrl+down')
             cv2.putText(frame, "VOLUME -5", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif (distance[2] < 0.08):
             vlc_control('right')
             cv2.putText(frame, "FORWARD +10sec", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif (distance[3] < 0.08):
             vlc_control('left')
             cv2.putText(frame, "BACKWARD -10sec", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif (distance[4] < 0.2):
             vlc_control('space')
        
        
    # Display the frame
    cv2.imshow("Hand Landmarks", frame)
    
    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close windows
cap.release()
cv2.destroyAllWindows()
