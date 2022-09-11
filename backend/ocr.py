import keras_ocr


class Ocr:
    def straighten_box(self, box):
        return [
            [int(box[0][0]), int(box[0][1])],
            [int(box[1][0]), int(box[1][1])],
            [int(box[2][0]), int(box[2][1])],
            [int(box[3][0]), int(box[3][1])],
        ]

    def get_text(self, image_path):
        pipeline = keras_ocr.pipeline.Pipeline()
        img_ocr = keras_ocr.tools.read(image_path)
        prediction_groups = pipeline.recognize([img_ocr])

        boxes = []
        text_strs = []

        for prediction in prediction_groups[0]:
            x0, y0 = prediction[1][0]
            x1, y1 = prediction[1][1]
            x2, y2 = prediction[1][2]
            x3, y3 = prediction[1][3]
            boxes.append(self.straighten_box([[x0, y0], [x1, y1], [x2, y2], [x3, y3]]))
            text_strs.append(prediction[0])

        return boxes, text_strs, img_ocr