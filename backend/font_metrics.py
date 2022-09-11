from PIL import Image, ImageFont
import cv2

class FontFitter:
    """
    l = left, r = right, t = top, b = bottom
    [[ltx, lty], [rtx, rty], [rbx, rby], [lbx, lby]]
    """
    def _get_box_dims(self, box):
        return (
            box[1][0] - box[0][0],
            box[2][1] - box[0][1]
        )

    """
    [left, top, right, bottom] => [[ltx, lty], [rtx, rty], [rbx, rby], [lbx, lby]]
    """
    def _boxify(self, box):
        return [
            [box[0], box[1]], [box[2], box[1]], [box[2], box[3]], [box[0], box[3]]
        ]

    def _normalize_box(self, box):
        return [
            [0, 0],
            [box[1][0] - box[0][0], 0],
            [max(box[2][0] - box[1][0], box[1][0] - box[0][0]), max(box[2][1] - box[1][1], 0)],
            [0, box[2][1] - box[1][1]]
        ]

    def _measure_text(self, box, text_str, font_name):
        box_width, box_height = box_dims = self._get_box_dims(box)
        img = Image.new('RGB', box_dims, 0)

        font = ImageFont.load_default()

        return self._boxify(font.getbbox(text_str))

    def get_optimal_font_scale(self, text_str, width):
        for scale in reversed(range(0, 60, 1)):
            textSize = cv2.getTextSize(text_str, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale / 10, thickness=1)
            new_width = textSize[0][0]
            if new_width <= width:
                return scale / 10
        return 1

    def _box_fits(self, a, b):
        return a[0][0] <= b[0][0] \
            and a[0][1] <= b[0][1] \
            and a[1][0] >= b[1][0] \
            and a[1][1] <= b[1][1] \
            and a[2][0] >= b[2][0] \
            and a[2][1] >= b[2][1] \
            and a[3][0] <= b[3][0] \
            and a[3][1] >= b[3][1]

    def _ellipsis_text(self, text_str, offset_back):
        return text_str[:-offset_back] + '...'

    def fit_text(self, box, text_str, font_name):
        normalized_box = self._normalize_box(box)
        ellipsis_lvl = 3
        measurement = self._measure_text(box, text_str, font_name)

        while self._box_fits(normalized_box, measurement) is False:
            ellipsis_lvl = ellipsis_lvl + 1
            measurement = self._measure_text(box, self._ellipsis_text(text_str, ellipsis_lvl), font_name)

        text = self._ellipsis_text(text_str, ellipsis_lvl)
        font_size = self.get_optimal_font_scale(text, self._get_box_dims(box)[0])

        return box, text, font_size