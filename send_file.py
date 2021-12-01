
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
import boto3
app = Flask(__name__)


# Use the temporary credentials that AssumeRole returns to make a
# connection to Amazon S3
s3_resource = boto3.resource('s3')


BUCKET_NAME = 'phutv12-final-audit-bucket'

@app.route('/')
def home():
    return render_template("file_upload_to_s3.html")


@app.route('/upload', methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)
            s3_resource.meta.client.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key=filename
            )
            msg = "Upload Done ! "

    return render_template("file_upload_to_s3.html", msg=msg)


if __name__ == "__main__":

    app.run(debug=True)
