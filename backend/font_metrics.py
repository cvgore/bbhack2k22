from PIL import Image, ImageFont

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

    def _measure_text(self, box, text_str, font_name, font_size):
        box_width, box_height = box_dims = self._get_box_dims(box)
        img = Image.new('RGB', box_dims, 0)

        font = ImageFont.load_default()

        return font.getbbox(text_str)

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

    def fit_text(self, box, text_str, font_name, font_size):
        ellipsis_lvl = 3
        measurement = self._measure_text(box, text_str, font_name, font_size)

        while self._box_fits(box, measurement) is False:
            ellipsis_lvl = ellipsis_lvl + 1
            measurement = self._measure_text(box, self._ellipsis_text(text_str, ellipsis_lvl), font_name, font_size)

        return box, text_str