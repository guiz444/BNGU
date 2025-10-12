# 蓝色箭头灯条目标检测项目

## 项目目标
本项目旨在实现对图像中蓝色箭头灯条的自动检测与框选。通过颜色分割、形态学处理和轮廓分析，实现目标的可视化标注，并保存检测结果。

---

## 检测方法概览
项目共包含三种检测策略，对应三个版本代码：

| 版本 | 方法 | 特点 | 优化点 |
|------|------|------|------|
| v1 | 直接使用 `boundingRect` | 对每个轮廓生成水平矩形 | 速度快，代码简洁，但对斜放箭头框不准 |
| v2 | `approxPolyDP` 多边形近似 + `boundingRect` | 使用多边形拟合轮廓，再生成矩形 | 对不规则轮廓更精确，减少过度框选，但略慢 |
| v3 | `minAreaRect` 最小旋转矩形 | 生成旋转矩形框，可匹配任意角度 | 对斜放箭头检测准确，结果更紧凑，适合多方向目标 |

---

## 共通处理流程
1. **读取图像**  
```python
img = cv2.imread(img_path)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
```

2. **蓝色颜色分割**
```python
lower_blue = np.array([90, 30, 180], dtype=np.uint8)
upper_blue = np.array([140, 255, 255], dtype=np.uint8)
mask = cv2.inRange(hsv, lower_blue, upper_blue)
```

3. **形态学闭操作**
```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
```

4. **轮廓检测**
```python
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

5. **目标筛选与绘制**

* 过滤小面积区域

* 根据版本不同生成矩形或多边形框

* 绘制在原图上并保存

---

## 版本核心代码示例
### v1 - 水平矩形框（Bounding Rect）
```python
for cnt in contours:
    if cv2.contourArea(cnt) < 80:
        continue
    x, y, w, h = cv2.boundingRect(cnt)
    if w < 5 or h < 5:
        continue
    cv2.rectangle(result_img, (x, y), (x+w, y+h), (0,0,255), 2)
```

### v2 - 多边形近似 + 矩形框
```python
epsilon = 0.03 * cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)
x, y, w, h = cv2.boundingRect(approx)
cv2.rectangle(result_img, (x, y), (x+w, y+h), (0,0,255), 2)
```

###v3 - 最小旋转矩形
```python
rect = cv2.minAreaRect(cnt)
(x, y), (w, h), angle = rect
if w < 5 or h < 5:
    continue
box = cv2.boxPoints(rect)
box = box.astype(np.int32)
cv2.drawContours(result_img, [box], 0, (0,0,255), 2)
```

--- 
## 优化点总结

* 1.颜色分割优化
** HSV阈值可通过可视化工具调整，以覆盖不同亮度和环境光条件。

* 2.噪声过滤
** 使用面积过滤和形态学闭操作，可减少小杂点干扰。

* 3.框选方式优化
** v3 的最小旋转矩形可准确匹配斜向目标，适合复杂场景。

* 4.结果可视化与保存
** 文件命名加时间戳，避免覆盖，并便于批量处理。

---

## 使用示例
```python
from detect_blue_light_arrow_v3 import detect_blue_light_arrow

mask, result_img, results = detect_blue_light_arrow("img2.png")
```
* 输出结果为：
** mask：二值掩膜
** result_img：带矩形或多边形标注的图像
** results：检测到的箭头区域信息
