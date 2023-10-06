#! python3

import sys
import os
from PIL import Image

MAX_WIDTH = 2500  # Change this to your desired maximum width
MAX_HEIGHT = 1600  # Change this to your desired maximum height

def resize_image(input_path, output_path, max_width, max_height):
    print(f'Processing file {output_path}')
    try:
        # Open the image file
        with Image.open(input_path) as img:
            width, height = img.size

            if width > height:
                # Landscape orientation
                print(f"Saved image using max_width as reference.")
                new_width = min(max_width, width)
                new_height = int(height * (new_width / width))
            elif height > width:
                # Portrait orientation
                print(f"Saved image using max_height as reference.")
                new_height = min(max_height, height)
                new_width = int(width * (new_height / height))
            else:
                print(f"Saved image with same dimensions to save space.")
                new_height = height
                new_width = width

            # Resize the image proportionally
            img.thumbnail((new_width, new_height))

            # Check the original image format
            original_format = img.format
            if original_format is None or original_format.lower() != "jpeg":
                # Convert to JPEG format
                img = img.convert("RGB")

            # Save as JPEG
            img.save(output_path, "JPEG")
            return True

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def process_directory(input_dir):
    output_dir = os.path.join(input_dir, "resized")
    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for file_name in files:
            input_path = os.path.join(root, file_name)

            if '/resized/' in input_path:
                continue

            if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                output_path = os.path.join(output_dir, file_name)
                try:
                    resize_image(input_path, output_path, MAX_WIDTH, MAX_HEIGHT)

                except Exception as e:
                    print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python resize_image.py <input_path>")
        sys.exit(1)

    input_path = sys.argv[1]

    if not os.path.exists(input_path):
        print("Error: The provided path does not exist.")
        sys.exit(1)

    if os.path.isfile(input_path):
        # Process a single file
        file_name, file_extension = os.path.splitext(input_path)
        output_path = os.path.join(os.path.dirname(input_path), "resized", f"{file_name}_adjusted{file_extension}")
        try:
            resize_image(input_path, output_path, MAX_WIDTH, MAX_HEIGHT)

        except Exception as e:
            print(f"Error: {e}")
    elif os.path.isdir(input_path):
        # Process a directory
        confirm = input(f"Do you want to resize all images in '{input_path}' and save them in a 'resized' folder? (yes/no): ").lower()
        if confirm == "yes":
            process_directory(input_path)
        else:
            print("Operation canceled.")
    else:
        print("Error: The provided path is neither a file nor a directory.")
