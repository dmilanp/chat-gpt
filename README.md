
How to

BUSINESS_NAME=casona_cedros
BUSINESS_TYPE=hotel
TEMP_PATH="$BUSINESS_NAME/$BUSINESS_TYPE"
TARGET_DIR="/Users/diegomilan/Desktop/luxtay_resources/businesses/$TEMP_PATH"
echo $TARGET_DIR


~/Documents/chat-gpt/resize_image.py $TARGET_DIR

~/Documents/chat-gpt/upload_s3_dir.py --bucket-name luxtay.prod --bucket-path $TEMP_PATH  --directory $TARGET_DIR/resized