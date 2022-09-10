class TextReader:
    def __init__(self, image_name, model_name, in_line=True):
        self.image_name = image_name
        self.model_name = model_name
        self.in_line = in_line

    def read_text(self):
        # Read the data
        text = self.model_name.readtext(self.image_name, detail=0, paragraph=self.in_line)

        # Join texts writing each text in new line
        return '\n'.join(text)