#!/usr/bin/env python3

import os
import requests
import random
import string
import argparse
import mimetypes

UNSPLASH_API_KEY = os.environ.get('UNSPLASH_API_KEY')
if not UNSPLASH_API_KEY:
    print("Error: Unsplash API key not set in the environment")
    exit(1)

def main():
    parser = argparse.ArgumentParser(description='Download images from Unsplash.')
    parser.add_argument('query', metavar='search term', type=str,
                        help='the search term to use')
    parser.add_argument('num_images', metavar='num_images', type=int,
                        help='the number of images to download')
    args = parser.parse_args()

    # Generate a random directory name
    base_path = '/Users/diegomilan/Desktop/'
    directory_name = base_path + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    os.mkdir(directory_name)

    # Download the specified number of images from Unsplash
    for i in range(args.num_images):
        photo_url = get_random_photo_url(args.query)
        photo_filename = photo_url.split("/")[-1]
        photo_extension = mimetypes.guess_extension(requests.head(photo_url).headers['content-type'])
        with open(os.path.join(directory_name, photo_filename + photo_extension), 'wb') as f:
            f.write(requests.get(photo_url).content)

    print(f"Images downloaded to {directory_name}")

def get_random_photo_url(query):
    url = f"https://api.unsplash.com/photos/random?client_id={UNSPLASH_API_KEY}&query={query}"
    response = requests.get(url)
    response_json = response.json()
    return response_json['urls']['regular']

if __name__ == '__main__':
    main()
