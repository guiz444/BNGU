import cv2
import numpy as np
from imagepoints import detect_black_shapes_on_yellow

# ---------------- 相机参数 ----------------
cameraMatrix = np.array([[1.174511689696492e+03, 0, 6.386366942819570e+02],
                         [0, 1.175197092436960e+03, 8.627497739086036e+02],
                         [0, 0, 1]], dtype=np.float32)
distCoeffs = np.array([0.103247081556123, 0.225565033862951, 0, 0, 0], dtype=np.float32)

# 物体 3D 坐标（左上、左下、右上、右下）
objectPoints = np.array([
    [-100, -75, 0],
    [-100, 75, 0],
    [100, -75, 0],
    [100, 75, 0],
], dtype=np.float32)

axis_length = 50  # 坐标轴长度
jump_threshold = 40  # 跳动阈值
prev_imagePoints = None

cap = cv2.VideoCapture("stone.mp4")
if not cap.isOpened():
    print("无法打开视频")
    exit()

# 获取视频尺寸和帧率
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 输出视频 writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 格式
out = cv2.VideoWriter("output_result.mp4", fourcc, fps, (frame_width, frame_height))

first_frame_saved = False
paused = False

while True:
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break

        result_img, squares = detect_black_shapes_on_yellow(frame)

        # 保存第一帧检测结果
        if not first_frame_saved and squares:
            cv2.imwrite("first_frame_detected.png", result_img)
            first_frame_saved = True

        draw_axes = False
        if len(squares) == 4:
            imagePoints = np.array([
                [squares[0][0], squares[0][1]],  # 左上
                [squares[1][0], squares[1][1] + squares[1][3]],  # 左下
                [squares[2][0] + squares[2][2], squares[2][1]],  # 右上
                [squares[3][0] + squares[3][2], squares[3][1] + squares[3][3]]  # 右下
            ], dtype=np.float32)

            # 跳动过滤
            if prev_imagePoints is None:
                draw_axes = True
            else:
                dist = np.linalg.norm(imagePoints - prev_imagePoints, axis=1).mean()
                if dist < jump_threshold:
                    draw_axes = True

            prev_imagePoints = imagePoints.copy()

            # SolvePnP + 绘制坐标轴
            if draw_axes:
                retval, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs)
                if retval:
                    cv2.drawFrameAxes(frame, cameraMatrix, distCoeffs, rvec, tvec, axis_length)

            # 绘制角点
            for pt in imagePoints:
                cv2.circle(frame, tuple(pt.astype(int)), 5, (0, 255, 255), -1)

        # 写入输出视频
        out.write(frame)

    cv2.imshow("3D Pose Visualization", frame)

    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC退出
        break
    elif key == 32:  # 空格暂停/继续
        paused = not paused
    elif key == ord('s') or key == ord('S'):  # 保存当前帧
        timestamp = cv2.getTickCount()
        filename = f"saved_frame_{timestamp}.png"
        cv2.imwrite(filename, frame)
        print(f"保存当前帧: {filename}")

cap.release()
out.release()
cv2.destroyAllWindows()
