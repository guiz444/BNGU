import cv2
import numpy as np


def hsv_mask_exact_tool(image_path):
    """
    HSV掩膜调试工具（支持多点点击，自动计算最小/最大HSV）

    参数：
    - image_path: 图像路径

    返回：
    - lower_hsv: HSV_min np.array([H, S, V])
    - upper_hsv: HSV_max np.array([H, S, V])
    """
    img_bgr = cv2.imread(image_path)

    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    clone = img_bgr.copy()

    hsv_points = []
    point_coords = []

    def pick_hsv(event, x, y, flags, param):
        nonlocal hsv_points, point_coords
        if event == cv2.EVENT_LBUTTONDOWN:
            hsv_val = img_hsv[y, x]
            hsv_points.append(hsv_val)
            point_coords.append((x, y))
            print(f"Clicked HSV: {hsv_val}")

    cv2.namedWindow("HSV Mask Tool")
    cv2.setMouseCallback("HSV Mask Tool", pick_hsv)

    while True:
        display_img = clone.copy()

        for (x, y) in point_coords:
            cv2.circle(display_img, (x, y), 5, (0, 0, 255), -1)  # 红点标记


        if hsv_points:
            hsv_array = np.array(hsv_points)

            lower_hsv = hsv_array.min(axis=0)
            upper_hsv = hsv_array.max(axis=0)


            mask = cv2.inRange(img_hsv, lower_hsv, upper_hsv)


            overlay = display_img.copy()
            overlay[mask > 0] = (0, 0, 255)  # 红色覆盖
            display_img = cv2.addWeighted(overlay, 0.5, display_img, 0.5, 0)

        cv2.imshow("HSV Mask Tool", display_img)


        if cv2.getWindowProperty("HSV Mask Tool", cv2.WND_PROP_VISIBLE) < 1:
            break
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()

    if hsv_points:
        lower_hsv = hsv_array.min(axis=0)
        upper_hsv = hsv_array.max(axis=0)

        print(f"Final HSV range: {lower_hsv} ~ {upper_hsv}")
        return lower_hsv, upper_hsv
    else:
        print("未点击任何点")
        return None, None


