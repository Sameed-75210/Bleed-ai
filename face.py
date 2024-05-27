import cv2
import mediapipe

def detect_face(image):
    mp_face_detection = mediapipe.solutions.face_detection
    mp_drawing = mediapipe.solutions.drawing_utils
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = face_detection.process(image_rgb)

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = image.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cropped_face = image[y:y+h, x:x+w]

            cropped_face_rgb = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)

            mp_face_mesh = mediapipe.solutions.face_mesh
            face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

            landmarks = face_mesh.process(cropped_face_rgb)
            if landmarks.multi_face_landmarks:
                for face_landmarks in landmarks.multi_face_landmarks:
                    for landmark in face_landmarks.landmark:
                        x_lm, y_lm = int(landmark.x * w), int(landmark.y * h)
                        cv2.circle(cropped_face, (x_lm, y_lm), 2, (255, 0, 0), -1)
    
    return image, cropped_face




