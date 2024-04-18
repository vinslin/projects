import streamlit as st
import cv2 
import mediapipe as mp
import numpy as np
from PIL import Image

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose



def board(angle, workout):
    angle = angle
    x=workout
    global counter # Initialize the counter variable
    global stage 
    if x==0:
       if angle > 160:
          stage = "DOWN"
       if angle < 50 and stage == 'DOWN':
          stage = "UP"
          counter += 1
    if x==1:
        if angle > 160:
          stage = "UP"
        if angle < 100 and stage == 'UP':
          stage = "DOWN"
          counter += 1

    return stage, counter

    
def calculate_angle(a, b, c):
    a = np.array(a) 
    b = np.array(b) 
    c = np.array(c) 
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle 

def start_video(workout):
    temp = workout
    cap = cv2.VideoCapture(0)
   
    
    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("Error: Failed to capture frame.")
                break
                
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)




           
            try:
                landmarks = results.pose_landmarks.landmark
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                angle = calculate_angle(shoulder, elbow, wrist)
                cv2.putText(image, str(angle), tuple(np.multiply(elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                
                stage, counter=board(angle,temp)
                 # Render curl counter
                cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)
                cv2.putText(image, 'REPS', (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, 'STAGE', (65, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, stage, (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

            except:
                pass
            
                       
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

st.markdown("<h1 style='text-align: center;'>AI WORKOUT TRACKER</h1>", unsafe_allow_html=True)
st.title('')
image = Image.open(r"C:\Users\ELCOT\pose\0_OQQk0E3tHNBd-xn7.webp")
st.image(image, use_column_width=True)


st.title('')
st.title('')
st.title('')

st.markdown("<h3 style='text-align: center;'>DUMPLES</h3>", unsafe_allow_html=True)
st.title('')
image1 = Image.open(r"C:\Users\ELCOT\pose\images.jfif")
st.image(image1, use_column_width=True)

#assign variables
counter =0
stage = None

if st.button('START'):
    x = start_video(0)


st.title('')
st.title('')
st.title('')

st.markdown("<h3 style='text-align: center;'>PUSH UPS</h3>", unsafe_allow_html=True)
st.title('')
image2 = Image.open(r"C:\Users\ELCOT\pose\push-ups-main.jpg")
st.image(image2, use_column_width=True)

if st.button('START '):
    x = start_video(1)

