import cv2
import mediapipe as mp
import math
import keyboard
import time
import pyautogui

time.sleep(10)
# Function to control VLC with delay

# Initialize MediaPipe HandPose model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

# Initialize variables for storing previous thumb position
prev_thumb_x, prev_thumb_y = 0, 0 # Change this to the index of the second hand point

#import pyautogui

def move_cursor(thumb_x, thumb_y, prev_thumb_x, prev_thumb_y, scale_factor):
    try:
        # Calculate movement of the thumb relative to its previous position
        thumb_dx = thumb_x - prev_thumb_x
        thumb_dy = thumb_y - prev_thumb_y

        # Scale the thumb movement by the specified factor
        scaled_thumb_dx = thumb_dx * scale_factor
        scaled_thumb_dy = thumb_dy * scale_factor

        # Move the cursor on the screen based on the scaled thumb movement
        pyautogui.move(scaled_thumb_dx, scaled_thumb_dy)

        # Update previous thumb position
        return thumb_x, thumb_y
    except Exception as e:
        return prev_thumb_x, prev_thumb_y

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
        distance = [calculate_distance(hand_landmarks, 8, 12),calculate_distance(hand_landmarks, 4, 8),calculate_distance(hand_landmarks, 4, 12),calculate_distance(hand_landmarks, 4, 16),calculate_distance(hand_landmarks, 4, 20),calculate_distance(hand_landmarks, 0, 20)]
        if (distance[0] < 0.03):
             thumb_landmark = hand_landmarks.landmark[4]
             thumb_x, thumb_y = thumb_landmark.x * frame.shape[1], thumb_landmark.y * frame.shape[0]
             # Move the cursor using the function
             prev_thumb_x, prev_thumb_y = move_cursor(thumb_x, thumb_y, prev_thumb_x, prev_thumb_y,1.75)



        elif (distance[1] < 0.07):
             pyautogui.click()
             time.sleep(1)
        elif (distance[2] < 0.08):
             pyautogui.rightClick()
             time.sleep(1)
        elif (distance[3] < 0.08):
             pyautogui.scroll(25)
        elif (distance[4] < 0.08):
             pyautogui.scroll(-25)
        elif (distance[5] < 0.2):
             pyautogui.doubleClick()
             time.sleep(1)
        # Display distance on the frame
        cv2.putText(frame, f"Distance: {(distance[0])}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
    # Display the frame
    cv2.imshow("Hand Landmarks", frame)
    
    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close windows
cap.release()
cv2.destroyAllWindows()
