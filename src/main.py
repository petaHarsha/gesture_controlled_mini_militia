import cv2
from gesture_detector import GestureDetector
from game_controller import GameController

def main():
    detector = GestureDetector()
    controller = GameController()
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Camera error!")
            break

        frame = cv2.flip(frame, 1)
        results = detector.detect_gestures(frame)

        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                handedness = results.multi_handedness[hand_idx].classification[0].label
                is_right_hand = (handedness == "Right")

                if is_right_hand:
                    # Right Hand: Shooting/Melee
                    if detector.are_all_fingers_open(hand_landmarks):
                        controller.mouse_action("down")
                    else:
                        controller.mouse_action("up")

                    if detector.is_thumb_open(hand_landmarks):
                        controller.press_key(controller.key_bindings["melee"])
                else:
                    # Left Hand: Movement/Bombs/Jetpack
                    wrist_x = hand_landmarks.landmark[0].x
                    if wrist_x < 0.3:
                        controller.press_key(controller.key_bindings["move_left"])
                    elif wrist_x > 0.7:
                        controller.press_key(controller.key_bindings["move_right"])
                    else:
                        controller.release_key(controller.key_bindings["move_left"])
                        controller.release_key(controller.key_bindings["move_right"])

                    if detector.is_thumb_open(hand_landmarks):
                        controller.press_key(controller.key_bindings["bomb"])
                    if detector.are_all_fingers_open(hand_landmarks):
                        controller.press_key(controller.key_bindings["jetpack"])
        else:
            controller.release_all_keys()

        cv2.imshow("Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
