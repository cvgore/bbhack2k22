from textReader import TextReader
from easyocr import Reader
testImage = "images-Samples/synonym_500x240.png"
reader_en = Reader(['en'])

textReader = TextReader(testImage, reader_en, True)

myText = textReader.read_text()
#iterate through the myText
for line in myText:
    print(line)


