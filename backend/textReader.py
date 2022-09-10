class TextReader:
    def __init__(self, image_name, model_name, in_line=True):
        self.image_name = image_name
        self.model_name = model_name
        self.in_line = in_line

    def read_text(self):
        # Read the data
        textTuple = self.model_name.readtext(self.image_name, detail=1)

        textList = []

        # Delete confidence score from data and add to list

        for data in textTuple:
            data = data[:-1]
            textList.append(data)

        return textList