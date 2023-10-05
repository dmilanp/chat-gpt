#! python3

import os
import boto3
import sys
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

            if prefix:
                prefix += '-'

            s3_path = os.path.join(target_folder, prefix + str(i))
            
            try:
                s3.upload_file(local_path, bucket, s3_path, ExtraArgs={'ContentType': content_type})
                url = f"https://s3.amazonaws.com/{bucket}/{s3_path}"
                print(f'"{url}",')
            except FileNotFoundError:
                print(f"{local_path} not found.")
            except NoCredentialsError:
                print("Credentials not available")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store_true', help='Use command line arguments instead of interactive input')
    # Shortcut mode
    parser.add_argument('-s', help='Shortcut filepath')
    parser.add_argument('-d', help='Delimiter word')
    # Regular params mode
    parser.add_argument('--bucket-name', help='Name of the S3 bucket')
    parser.add_argument('--bucket-path', help='Directory name to create inside bucket_path_base')
    parser.add_argument('--prefix', help='Prefix for new files')
    parser.add_argument('--directory', help='Full path of the directory to upload')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    default_bucket = os.environ.get('DEFAULT_BUCKET')
    bucket_path_base = 'application/images'

    if args.p:
        if args.s and args.d:
            rest = args.s.split(args.d)[1]
            bucket_path_dir = f'{args.d}{rest}'
            prefix = bucket_path_dir.split('/')[-1]
            directory = args.s
        else:
            bucket_path_dir = args.bucket_path
            prefix = args.prefix
            directory = args.directory

        bucket_name = args.bucket_name or default_bucket
        bucket_path_full = f"{bucket_path_base}/{bucket_path_dir}"

        # Confirm before proceeding
        print("\nPlease confirm the following inputs:")
        print(f"S3 Bucket Name: {bucket_name}")
        print(f"Bucket Path Directory: {bucket_path_full}")
        print(f"Prefix for New Files: {prefix}")
        print(f"Directory to Upload: {directory}")

        confirmation = input('Are you sure you want to proceed with the provided arguments? (y/n): ')
        if confirmation.lower() != 'y':
            print('Aborted.')
            exit()

        if not bucket_path_dir:
            print('Missing bucket_path_dir.')
            exit()
        if not prefix:
            prefix = ''
        if not directory:
            print('Missing directory.')
            exit()


    else:
        bucket_name = input(f'\nEnter the name of the S3 bucket, press enter for default ("{default_bucket}")\n')
        if not bucket_name:
            print(default_bucket)
            bucket_name = default_bucket

        bucket_path_dir = input(f'\nEnter the directory name. Will create "{bucket_path_base}/YOUR_NAME"\n')

        bucket_path_full = f"{bucket_path_base}/{bucket_path_dir}"

        prefix = input(f'\nEnter the prefix for new files (dash separated, no trailing dash)\n')

        directory = input("\nEnter the full path of the directory to upload: \n")

    upload_to_aws(directory, bucket_name, bucket_path_full, prefix)
