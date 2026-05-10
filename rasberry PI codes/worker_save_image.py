import time
import os
import re
import glob



# set logs for reading new images
def log(msg, LOG_FILE):
    timestamp = time.strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def recreate_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return
    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        if os.path.isfile(item_path):
            os.remove(item_path)

    os.rmdir(path)
    os.makedirs(path)

def check_reqs(LOG_FILE, IMAGES_FOLDER, DESTINATION_FOLDER, PLATE_NUMBER_RESULT):
    # check file writing
    try:
        with open(LOG_FILE, "w") as f:
            f.write("=== Image Save Worker started ===\n")
    except Exception as e:
        return "ERR(WSI):-log can't reach"

    log("Step 1 OK: Logging works.", LOG_FILE)

    # check file/folder paths
    log(f"Step 2: Checking paths...", LOG_FILE)
    log(f"  IMAGES_FOLDER exists:  {os.path.exists(IMAGES_FOLDER)}", LOG_FILE)
    log(f"  IMAGES_FOLDER exists:  {os.path.exists(DESTINATION_FOLDER)}", LOG_FILE)
    log(f"  IMAGES_FOLDER exists:  {os.path.exists(PLATE_NUMBER_RESULT)}", LOG_FILE)

    log("Step 3 OK: Folders ready.", LOG_FILE)


    # main loop of worker
    log("Step 4: Entering main loop...", LOG_FILE)

def save_image(LOG_FILE, IMAGES_FOLDER, DESTINATION_FOLDER, PLATE_NUMBER_RESULT):
    try:
        images = []
        for t in ["*.png", "*.jpg", "*.jpeg"]:
            images += glob.glob(os.path.join(IMAGES_FOLDER, t))

        if not images:
            log(f"ERROR: No images in {IMAGES_FOLDER}")
            return "ERR(WSI):-No image!"
        else:
            log(f"Images found: {len(images)}", LOG_FILE)

            # detect front and rear damage
            log('start moving new images from source to destination', LOG_FILE)

            # patterns for get image name and ext
            pattern = r'([^\\/]+)\.(png|jpg)'
            log(f'{images}', LOG_FILE)

            # read license number
            with open(PLATE_NUMBER_RESULT, "r") as f:
                license_number = f.read().strip()  

            # check folder
            recreate_folder(os.path.join(DESTINATION_FOLDER, license_number))
            log('recreated the destination folder', LOG_FILE)

            for image in images:
                log(f'saving {image}', LOG_FILE)
                matches = re.findall(pattern, image)
                image = matches[0][0] +'.'+ matches[0][1] 
                source_path = os.path.join(IMAGES_FOLDER, image)
                image = license_number + '\\' + image # add destination folder
                destination_path = os.path.join(DESTINATION_FOLDER, image)
                os.rename(source_path, destination_path)

                log(f'{image} saved!', LOG_FILE) 
            return "OK"                  

    except Exception as e:
        return "ERR(WSI):-check func!" 


