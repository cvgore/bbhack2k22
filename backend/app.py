import io
import random
import string
import logging

import cv2
import matplotlib.pyplot as plt
from zipfile import ZipFile
from tempfile import TemporaryFile
from flask import Flask, request, make_response, send_file
from werkzeug.utils import secure_filename

import font_metrics
import translator
from datetime import datetime
import deleteTextInImage as dtii
from ocr import Ocr

app = Flask(__name__)
tr = translator.Translator()
ff = font_metrics.FontFitter()
ocr = Ocr()


@app.route("/", methods=['POST'])
def hello_world():
    images = request.files.getlist('images')
    tr_data = request.files.getlist('translation')
    timestamp = datetime.now().timestamp()
    hash = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.hexdigits) for _ in range(8))

    images_to_process = []
    translations_to_process = []

    for i, file in enumerate(images):
        path = f"../var/uploads/image_{timestamp}_{hash}_{i}.png"
        images_to_process.append(path)
        file.save(path)
        logging.info(f'stored image at [{path}]')

    for i, file in enumerate(tr_data):
        path = f"../var/uploads/translation_{timestamp}_{hash}_{i}.csv"
        translations_to_process.append(path)
        file.save(path)
        logging.info(f'stored translation at [{path}]')

    for tr_file in translations_to_process:
        logging.info(f'loading translation [{tr_file}]')
        tr.load_translation_file(tr_file)

        for img_file in images_to_process:
            boxes, text_strs, img_ocr = ocr.get_text(img_file)
            for box, text_str in zip(boxes, text_strs):
                translated_text_str = tr.translate_text(text_str)
                box, text_str, font_size = ff.fit_text(box, translated_text_str, 'sample.ttf')

                img_ocr = dtii.deleteTextInImage(img_ocr, text_str, box)
                cv2.imwrite(img_file, img_ocr)

    tmpzip = io.BytesIO()
    with ZipFile(tmpzip, mode='x') as zipfile:
        for img_path in images_to_process:
            zipfile.write(img_path, secure_filename(images[0].filename))

        tmpzip.seek(0)

        response = make_response(tmpzip.read())
        response.headers.set('Content-Type', 'zip')
        response.headers.set('Content-Disposition', 'attachment', filename='sample.zip')
        return response