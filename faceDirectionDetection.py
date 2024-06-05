import cv2
import dlib
import numpy as np

# 顔の向きを推定する関数
def estimate_head_pose(shape):
    model_points = np.array([
        (0.0, 0.0, 0.0),             # 鼻の先端
        (0.0, -330.0, -65.0),        # 顎の先端
        (-225.0, 170.0, -135.0),     # 左目の左端
        (225.0, 170.0, -135.0),      # 右目の右端
        (-150.0, -150.0, -125.0),    # 左口角
        (150.0, -150.0, -125.0)      # 右口角
    ])

    # 画像の点
    image_points = np.array([
        shape[30],     # 鼻の先端
        shape[8],      # 顎の先端
        shape[36],     # 左目の左端
        shape[45],     # 右目の右端
        shape[48],     # 左口角
        shape[54]      # 右口角
    ], dtype="double")

    # カメラの内部パラメータ
    size = frame.shape
    focal_length = size[1]
    center = (size[1]/2, size[0]/2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")

    # 歪み係数
    dist_coeffs = np.zeros((4,1))

    # solvePnPで回転ベクトルと並進ベクトルを求める
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)

    # 回転ベクトルからオイラー角に変換
    rotation_matrix = cv2.Rodrigues(rotation_vector)[0]
    pose_matrix = cv2.hconcat((rotation_matrix, translation_vector))
    _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_matrix)

    return euler_angle

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        # 顔器官を検出
        shape = predictor(gray, face)
        
        # shapeからnumpy配列に変換
        shape = np.array([[p.x, p.y] for p in shape.parts()])

        # 顔の向きを推定
        euler_angle = estimate_head_pose(shape)

        # 正面を向いているかどうか判定
        is_frontal = abs(euler_angle[1]) < 20 and abs(euler_angle[2]) < 20

        # 結果を表示
        if is_frontal:
            color = (0, 255, 0) # 緑色で枠を描く
            text = "I Love You"   
        else:
            color = (0, 0, 255) # 赤色で枠を描く
            text = "Look At Me!" 

        # 顔の枠を描く
        cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), color, 2)

        # テキストを描く
        cv2.putText(frame, text, (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # フレームを表示
    cv2.imshow("LookAtMe", frame)

    # キー入力を待つ
    key = cv2.waitKey(1)
    # Escキーが押されたら終了
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
