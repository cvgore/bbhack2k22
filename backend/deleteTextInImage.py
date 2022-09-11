import cv2
import matplotlib.pyplot as plt
import keras_ocr
import math
import numpy as np


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

def deleteTextInImage(image_path):
        pipeline = keras_ocr.pipeline.Pipeline()
        img = keras_ocr.tools.read(image_path)
        prediction_groups = pipeline.recognize([img])
        mask = np.zeros(img.shape[:2], dtype="uint8")
        for prediction in prediction_groups[0]:
            x0, y0 = prediction[1][0]
            x1, y1 = prediction[1][1]
            x2, y2 = prediction[1][2]
            x3, y3 = prediction[1][3]
            x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
            x_mid1, y_mid1 = midpoint(x0, y0, x3, y3)
            width = (abs(x_mid0 - x_mid1))
            thickness = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
            cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mid1), 255, thickness)
            #here przeslac tekst do funkcji który zwrocilo tlumaczniee
            font_scale=get_optimal_font_scale("siemasiema", width)
            img_inpainted = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
            img_inpainted= cv2.putText(img_inpainted, "siemasiema", (x_mid1, y_mid1), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2)
            plt.imshow(img_inpainted)
            plt.show()

