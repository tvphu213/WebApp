
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
import boto3
app = Flask(__name__)


# create an STS client object that represents a live connection to the
# STS service
sts_client = boto3.client('sts')

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.
# assumed_role_object = sts_client.assume_role(
#     RoleArn="arn:aws:iam::424562183293:role/Ec2AccessToS3",
#     RoleSessionName="AssumeRoleSession1"
# )

# From the response that contains the assumed role, get the temporary
# credentials that can be used to make subsequent API calls
# credentials = assumed_role_object['Credentials']

# Use the temporary credentials that AssumeRole returns to make a
# connection to Amazon S3
s3_resource = boto3.resource('s3')
# aws_access_key_id=credentials['AccessKeyId'],
# aws_secret_access_key=credentials['SecretAccessKey'],
# aws_session_token=credentials['SessionToken'],


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
