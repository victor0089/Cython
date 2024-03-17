# app/__init__.py
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from cython_modules.image_processing import apply_grayscale_filter  # Updated import path

import os
import cv2

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = 'app/static/uploads/'
application.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in application.config['ALLOWED_EXTENSIONS']

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return redirect(url_for('process_image', filename=filename))

@application.route('/process/<filename>')
def process_image(filename):
    original_image_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
    image = cv2.imread(original_image_path)
    if image is not None:
        edited_image = apply_grayscale_filter(image)
        edited_image_path = os.path.join(application.config['UPLOAD_FOLDER'], 'edited_' + filename)
        cv2.imwrite(edited_image_path, edited_image)
        return render_template('result.html', original_image=filename, edited_image='edited_' + filename)
    return "Error: Unable to process image."

if __name__ == '__main__':
    application.run(debug=True)
