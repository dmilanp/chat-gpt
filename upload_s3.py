#! python3

import os
import boto3
import mimetypes

# Get AWS access key and secret key from shell environment
access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
default_bucket = os.environ.get('DEFAULT_BUCKET')


# Create S3 client with the given access and secret keys
s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

default_bucket_path = 'application/images'

# Get the S3 bucket name
bucket_name = input(f'Enter the name of the S3 bucket, press enter for default ("{default_bucket}")')
if not bucket_name:
    bucket_name = default_bucket

bucket_path  = input(f'Enter the path to upload the file to, press enter for default ("{default_bucket_path}")')
if not bucket_path:
    bucket_path = default_bucket_path

# Get the path to the file to upload
file_path = input("Enter the path to the file to upload: ")
content_type = mimetypes.guess_type(file_path)[0]

object_key = f'{bucket_path}/{os.path.basename(file_path)}'

# Upload the file to S3
s3.upload_file(file_path, bucket_name, object_key, ExtraArgs={'ContentType': content_type})

# Construct and print the URL of the uploaded asset
url = f"https://s3.amazonaws.com/{bucket_name}/{object_key}"
print(f"The URL of the uploaded asset is: {url}")
