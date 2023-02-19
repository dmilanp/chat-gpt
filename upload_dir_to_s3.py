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
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, local_directory)
            content_type = mimetypes.guess_type(local_path)[0]

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
    parser = argparse.ArgumentParser(description='Upload files from local directory to S3')
    parser.add_argument('--bucket_name', type=str, help='S3 bucket name', required=True)
    parser.add_argument('--target_path', type=str, help='Target path in S3 bucket', required=True)
    parser.add_argument('--local_directory', type=str, help='Local directory path', required=True)
    parser.add_argument('--prefix', type=str, help='Prefix for renamed files', default='')

    args = parser.parse_args()

    upload_to_aws(args.local_directory, args.bucket_name, args.target_path, args.prefix)
