import cv2
import matplotlib.pyplot as plt
import keras_ocr
import math
import numpy as np
from zipfile import ZipFile



def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2) / 2)
    y_mid = int((y1 + y2) / 2)
    return x_mid, y_mid

def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 60, 1)):
        textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale/10, thickness=1)
        new_width = textSize[0][0]
        if (new_width <= width):
            print(new_width)
            return scale/10
    return 1

def deleteTextInImage(img_ocr, text_str, box):
    mask = np.zeros(img_ocr.shape[:2], dtype="uint8")
    x0, y0 = box[0]
    x1, y1 = box[1]
    x2, y2 = box[2]
    x3, y3 = box[3]
    x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
    x_mid1, y_mid1 = midpoint(x0, y0, x3, y3)
    width = int(abs(x_mid0 - x_mid1))
    thickness = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mid1), 255, thickness)
    font_scale = get_optimal_font_scale(text_str, width)
    img_inpainted = cv2.inpaint(img_ocr, mask, 7, cv2.INPAINT_NS)
    img_ocr = cv2.putText(img_inpainted, text_str, (x_mid1, y_mid1), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), 2)
    img_rgb = cv2.cvtColor(img_ocr, cv2.COLOR_BGR2RGB)
    return img_rgb


