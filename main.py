from datetime import datetime
import os
import time
import requests
import shutil

WORKING_DIRECTORY = os.path.realpath(__file__)
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
IMAGE_FOLDER_NAME = os.path.join(SCRIPT_PATH, "images")

def download_image(hour: str, savename: str) -> None:
    # Takes in an hour and downloads the image for that hour
    # do the request
    r = requests.get(f"https://live24.nu/sergelstorg/historik/sergelstorg_{hour}_1280.jpg", stream=True)
    if r.status_code == 200:
        savename = os.path.join(IMAGE_FOLDER_NAME, savename)

        # Save the data from the request 
        with open(savename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f) 

def main():
    print("running...")

    # ensure image folder exists
    if not os.path.isdir(IMAGE_FOLDER_NAME):
        os.mkdir(IMAGE_FOLDER_NAME)

    while True:
        # time.sleep(60)
        now = datetime.now()
        min = now.strftime("%M")
        h = now.strftime("%H")
        # We want to check in the middle of the hour to remove lagged updates
        # We also want to make sure to download the image
        # so we download between 30 and 32 to be absoultely sure
        if int(min) >= 30 and int(min) <= 32:
            # download the image
            full_filename = os.path.join(IMAGE_FOLDER_NAME, now.strftime("%Y-%m-%d_hour%H.jpeg"))
            download_image(h, full_filename)

            # do some logging
            hour_name = now.strftime("%d-%m-%Y hour: %H")
            print(f"saved file filename {hour_name}")

            # When we have downloaded the image, we do not want to download it again.
            # So we sleep for 5 minutes 
            time.sleep(300)
            # After those 5 minutes the time for downloading is passed

if __name__ == "__main__":
    main()
