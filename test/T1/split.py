import cv2
import numpy as np
from datetime import datetime
from T1.HSV_estimate import  hsv_mask_estimating_tool

img = cv2.imread("img1.png")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower, upper = hsv_mask_estimating_tool("img1.png")

if lower is None or upper is None:
    print("未选择颜色点，无法生成掩膜")
else:
    lower = np.array(lower, dtype=np.uint8)
    upper = np.array(upper, dtype=np.uint8)

    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_filename = f"img1_out_{timestamp}.png"

    cv2.imwrite(f"img1_out_{timestamp}.png", result)
    print(f"掩膜图保存成功：img1_out_{timestamp}.png")


