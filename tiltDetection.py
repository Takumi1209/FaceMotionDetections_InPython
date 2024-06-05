import cv2
import dlib
import numpy as np

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# 顔のランドマークを基に顔の傾きを計算する関数
def calculate_tilt(landmarks):
    # 目のランドマークの座標を取得
    left_eye = landmarks[36:42]
    right_eye = landmarks[42:48]

    # 両目の中心点を計算
    left_eye_center = np.mean(left_eye, axis=0).astype("int")
    right_eye_center = np.mean(right_eye, axis=0).astype("int")

    # 両目の中心点を結ぶ線の角度を計算
    dY = right_eye_center[1] - left_eye_center[1]
    dX = right_eye_center[0] - left_eye_center[0]
    angle = np.degrees(np.arctan2(dY, dX))

    return abs(angle)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    # 検出された顔に対して処理
    for face in faces:
        # 顔のランドマークを検出
        landmarks = predictor(gray, face)
        landmarks = np.array([[p.x, p.y] for p in landmarks.parts()])

        # 顔の傾きを計算
        tilt = calculate_tilt(landmarks)

        # 傾きを表示
        cv2.putText(frame, f"Tilt: {tilt:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # フレームを表示
    cv2.imshow('Frame', frame)

    # Escキーを押すと終了
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
