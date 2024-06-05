import cv2
import numpy as np
import dlib
import time

face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 頷きが検出された後の待機時間（秒）
wait_time = 1
# 最後に頷きが検出された時間
last_nod_time = 0

# 鼻の座標の変化量の閾値を設定
threshold = 10

# 頷きの回数をカウントする変数を初期化
nod_count = 0

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray)

    for face in faces:
        landmarks = landmark_predictor(gray, face)

        # 鼻の先端の座標を取得
        nose_x = landmarks.part(30).x
        nose_y = landmarks.part(30).y

        # 鼻の先端に赤い点を描く
        cv2.circle(frame, (nose_x, nose_y), 3, (0, 0, 255), -1)

        # 最初のフレームでは前の鼻の座標を初期化
        if 'prev_nose_x' not in locals():
            prev_nose_x = nose_x
            prev_nose_y = nose_y

        # 鼻の座標の変化量を計算
        diff_x = nose_x - prev_nose_x
        diff_y = nose_y - prev_nose_y

        # 前の鼻の座標を更新
        prev_nose_x = nose_x
        prev_nose_y = nose_y

        # 鼻の座標の変化量が閾値より大きければ、頷きと判定
    if diff_y > threshold:
    # 現在の時間が最後に頷きが検出されてから指定した時間以上経過しているか確認
        if time.time() - last_nod_time >= wait_time:
            nod_count += 1
            # 頷きが検出された時間を更新
            last_nod_time = time.time()

    # 頷きの回数を画面に表示
    cv2.putText(frame, f"Nod count: {nod_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 画像をウィンドウに表示
    cv2.imshow("Nod Detection", frame)

    # キー入力を待つ
    key = cv2.waitKey(1)
    # Escキーが押されたら終了
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
