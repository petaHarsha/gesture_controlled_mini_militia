import cv2
import mediapipe as mp
import numpy as np
import math

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        self.results = None

    def detect_gestures(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)
        return self.results

    @staticmethod
    def is_thumb_open(landmarks):
        thumb_tip = landmarks.landmark[4]
        index_base = landmarks.landmark[1]
        distance = math.dist((thumb_tip.x, thumb_tip.y), (index_base.x, index_base.y))
        return distance > 0.1

    @staticmethod
    def are_all_fingers_open(landmarks):
        finger_angles = [
            GestureDetector.calculate_finger_angle(landmarks, tip, pip, mcp)
            for tip, pip, mcp in [(8, 7, 5), (12, 11, 9), (16, 15, 13), (20, 19, 17)]
        ]
        return all(angle > 160 for angle in finger_angles)

    @staticmethod
    def calculate_finger_angle(landmarks, tip_idx, pip_idx, mcp_idx):
        # Vector math to check finger extension
        tip = np.array([landmarks.landmark[tip_idx].x, landmarks.landmark[tip_idx].y])
        pip = np.array([landmarks.landmark[pip_idx].x, landmarks.landmark[pip_idx].y])
        mcp = np.array([landmarks.landmark[mcp_idx].x, landmarks.landmark[mcp_idx].y])
        vec1, vec2 = tip - pip, pip - mcp
        return np.degrees(np.arccos(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
