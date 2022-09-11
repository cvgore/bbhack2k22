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

def deleteTextInImage(image_list):
    #foreach image in image_path
    for image in image_list:
        pipeline = keras_ocr.pipeline.Pipeline()
        img_ocr = keras_ocr.tools.read(image)
        prediction_groups = pipeline.recognize([img_ocr])
        mask = np.zeros(img_ocr.shape[:2], dtype="uint8")
        for prediction in prediction_groups[0]:
            x0, y0 = prediction[1][0]
            x1, y1 = prediction[1][1]
            x2, y2 = prediction[1][2]
            x3, y3 = prediction[1][3]
            x_mid0, y_mid0 = midpoint(x1, y1, x2, y2)
            x_mid1, y_mid1 = midpoint(x0, y0, x3, y3)
            width = int(abs(x_mid0 - x_mid1))
            thickness = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
            cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mid1), 255, thickness)
            #here przeslac tekst do funkcji który zwrocilo tlumaczniee
            font_scale = get_optimal_font_scale("eloo", width)
            img_inpainted = cv2.inpaint(img_ocr, mask, 7, cv2.INPAINT_NS)
            #here tez tekst i kolor i foncik
            img_ocr = cv2.putText(img_inpainted, "eloo", (x_mid1, y_mid1), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), 2)
            #do nagrania demko to poniżej
            #plt.imshow(img_ocr)
            #plt.show()
        img_rgb = cv2.cvtColor(img_ocr, cv2.COLOR_BGR2RGB)
        cv2.imwrite(image, img_rgb)

        zipObj = ZipFile('translated.zip', 'w')
    for edited_image in image_list:
        zipObj.write(edited_image)
    zipObj.close()
