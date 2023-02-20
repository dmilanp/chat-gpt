#! python3

import os
import boto3
from botocore.exceptions import NoCredentialsError
import argparse
import mimetypes


def upload_to_aws(local_directory, bucket, target_folder, prefix):
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    for root, dirs, files in os.walk(local_directory):
        for i, filename in enumerate(files):
            if filename in ['.DS_Store']:
                continue

            try:
                local_path = os.path.join(root, filename)
                relative_path = os.path.relpath(local_path, local_directory)
                content_type = mimetypes.guess_type(local_path)[0]
            except:
                print(f'An error occurred processing file "{filename}",')
                raise

            s3_path = os.path.join(target_folder, prefix + '-' + str(i))
            
            try:
                s3.upload_file(local_path, bucket, s3_path, ExtraArgs={'ContentType': content_type})
                url = f"https://s3.amazonaws.com/{bucket}/{s3_path}"
                print(f'"{url}",')
            except FileNotFoundError:
                print(f"{local_path} not found.")
            except NoCredentialsError:
                print("Credentials not available")


if __name__ == '__main__':
    default_bucket = os.environ.get('DEFAULT_BUCKET')
    default_bucket_path = 'application/images'

    # Get the S3 bucket name
    bucket_name = input(f'Enter the name of the S3 bucket, press enter for default ("{default_bucket}")')
    if not bucket_name:
        bucket_name = default_bucket

    bucket_path  = input(f'Enter the path to upload the file to, press enter for default ("{default_bucket_path}")')
    if not bucket_path:
        bucket_path = default_bucket_path

    prefix  = input(f'Enter the prefix for new files (dash separated)')

    # Get the path to the directory to upload
    directory = input("Enter the path to the directory to upload: ")

    upload_to_aws(directory, bucket_name, bucket_path, prefix)
