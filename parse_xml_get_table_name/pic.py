# import cv2
# import numpy as np
# from PIL import Image

# # 加载图片
# image_path = '/Users/mac/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/cdb9e070e666658f57da04d3c5858f63/Message/MessageTemp/f0c922643e8b59c9fec408420bdcfd68/Image/2.pic.jpg'  # 替换为你的图片路径
# image = cv2.imread(image_path)

# # 转换为HSV颜色空间，以便更好地识别黄色区域
# hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# # 定义黄色的HSV范围
# lower_yellow = np.array([20, 100, 100])
# upper_yellow = np.array([40, 255, 255])

# # 创建黄颜色的掩膜
# yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

# # 使用掩膜擦除黄色区域，将其填充为白色（或其他背景颜色）
# image[yellow_mask != 0] = [255, 255, 255]

# # 对文字区域进行处理，假设你已知大致位置 (x, y, width, height)
# # 使用矩形覆盖文字区域
# # 这里需要手动调整这些位置坐标来去除具体的文字区域
# text_box_area = (250, 200, 600, 250)  # 替换为你需要擦除文字的位置
# image[text_box_area[1]:text_box_area[3], text_box_area[0]:text_box_area[2]] = [255, 255, 255]

# # 将处理后的图片转换为PIL图像并保存
# output_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
# output_image_path = "processed_image.jpg"  # 输出路径
# output_image.save(output_image_path)

# print(f"处理后的图片已保存为 {output_image_path}")


import cv2
import pytesseract

# 加载图片
image_path = '/Users/mac/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/cdb9e070e666658f57da04d3c5858f63/Message/MessageTemp/f0c922643e8b59c9fec408420bdcfd68/Image/2.pic.jpg'  # 替换为你的图片路径

image = cv2.imread(image_path)

# 转换为灰度图像，提升OCR识别准确性
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用Tesseract进行文字识别，提取文本区域（bounding boxes）
# 识别并提取图片中的文字和对应的坐标
boxes = pytesseract.image_to_boxes(gray_image)

# 打印每个字符的位置
for box in boxes.splitlines():
    b = box.split()
    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    # 根据识别的文字区域生成text_box_area
    text_box_area = (x, image.shape[0] - h, w, image.shape[0] - y)  # 计算文本区域
    print(f"Detected text area: {text_box_area}")

    # 在图像上绘制一个矩形框，标出文字区域
    cv2.rectangle(image, (x, image.shape[0] - y), (w, image.shape[0] - h), (0, 255, 0), 2)

# 显示图像并保存
cv2.imshow("Image with detected text area", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
