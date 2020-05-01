from pathlib import Path
import boto3
import os
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from image.ImageUtil import ImageUtil

# Allowed Extensions to upload
ALLOWED_EXTENSIONS = {'.jpg', '.png', '.jpeg'}

app = Flask(__name__)

# Create Temp folder for uploaded files
uploadPath = Path('upload')
if not uploadPath.exists():
    uploadPath.mkdir()
app.config['UPLOAD_FOLDER'] = uploadPath.absolute()
# Maximum File size 2 MB
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    pass


@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        response = jsonify({'message': 'No File in request'})
        response.status_code = 400
        return response

    # Getting File from Request and checking it's extension
    file = request.files['file']
    if allowed_file(file.filename):

        # get water mark text
        text = request.form.get('text')

        # save file to tmp path
        filename = secure_filename(file.filename)
        filename = f'{uuid.uuid4()}{os.path.splitext(filename)[1].lower()}'
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

        # Create Image Util Instance
        image = ImageUtil(image_path)
        image.watermark(watermark_text=text, save_to=image_path)

        # saving to Amazon S3
        s3_resource = boto3.client('s3')
        s3_resource.upload_file(Filename=image_path, Bucket='python-image-storage', Key=filename)

        # Remove File After upload
        os.remove(image_path)

        # Return Response
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        response = jsonify({'message': f'You can just upload {ALLOWED_EXTENSIONS}'})
        response.status_code = 400
        return response


if __name__ == '__main__':
    app.run()
