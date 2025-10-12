import cv2 # 导入视觉库
img = cv2.imread('image.jpg') # 把引号内的文件名修改为你的图片名
cv2.imshow('test', img)
cv2.waitKey(0) # 显示图片直到有任何键盘点击操作