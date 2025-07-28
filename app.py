from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    images_and_text = []

    if request.method == 'POST':
        uploaded_files = request.files.getlist('images')

        for file in uploaded_files:
            if file.filename == '':
                continue

            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # OCR
            image = Image.open(filepath)
            text = pytesseract.image_to_string(image)

            images_and_text.append((filename, text))

        return render_template('index.html', data=images_and_text)

    return render_template('index.html', data=[])

if __name__ == '__main__':
    app.run(debug=True)
