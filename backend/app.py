from flask import Flask, request
from werkzeug.utils import secure_filename
import font_metrics
import translator

app = Flask(__name__)
tr = translator.Translator()


@app.route("/", methods=['POST'])
def hello_world():
    images = request.files['images']
    tr_data = request.files['translation_data']

    for file in images:
        file.path = f"../var/uploads/{secure_filename(file.filename)}"
        file.save(file.path)

    for file in tr_data:
        file.path = f"../var/uploads/{secure_filename(file.filename)}"
        file.save(file.path)

    tr.load_translation_file(tr_data[0].path)
    ff = font_metrics.FontFitter()
    ff.fit_text(..., tr.translate_text(...))


import deleteTextInImage as dtii

dtii.deleteTextInImage('zz.png')