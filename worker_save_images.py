import time
import os
import re

STOP_FILE      = r"E:\files\my projects\car_damage_system\data\stop.flag"
RESULT_FILE    = r"E:\files\my projects\car_damage_system\data\save_image_result.txt"
NEW_IMAGE_FLAG = r"E:\files\my projects\car_damage_system\data\new_image_to_save.flag"
LOG_FILE       = r"E:\files\my projects\car_damage_system\data\worker_save_image_log.txt"
IMAGES_FOLDER  = r"E:\files\my projects\car_damage_system\incoming"
DESTINATION_FOLDER = r"E:\files\my projects\car_damage_system\data\images"
PLATE_NUMBER_RESULT = r"E:\files\my projects\car_damage_system\data\detect_car_worker_plate_number.txt"

# check file writing
try:
    with open(LOG_FILE, "w") as f:
        f.write("=== Image Save Worker started ===\n")
except Exception as e:
    import sys
    sys.exit(f"FATAL: Cannot write log: {e}")

# set logs for reading new images
def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
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


log("Step 1 OK: Logging works.")

log("Step 2: Importing glob...")
try:
    import glob
    log("Step 2 OK: glob imported.")
except Exception as e:
    log(f"Step 2 FAILED: {e}")

# check file/folder paths
log(f"Step 3: Checking paths...")
log(f"  STOP_FILE exists:      {os.path.exists(STOP_FILE)}")
log(f"  NEW_IMAGE_FLAG exists: {os.path.exists(NEW_IMAGE_FLAG)}")
log(f"  IMAGES_FOLDER exists:  {os.path.exists(IMAGES_FOLDER)}")

os.makedirs(IMAGES_FOLDER, exist_ok=True)
log("Step 3 OK: Folders ready.")


# main loop of worker
log("Step 4: Entering main loop...")
loop_count = 0

while not os.path.exists(STOP_FILE):
    loop_count += 1

    # Log every 20 iterations so we know loop is alive
    if loop_count % 20 == 0:
        log(f"Loop alive (iteration {loop_count}). "
            f"Flag exists: {os.path.exists(NEW_IMAGE_FLAG)}")

    if os.path.exists(NEW_IMAGE_FLAG):
        log(f"FLAG DETECTED at iteration {loop_count}!")
        os.remove(NEW_IMAGE_FLAG) # if we detect new image, remove before starting
        log("Flag removed. Looking for images...")

        try:
            images = []
            for t in ["*.png", "*.jpg", "*.jpeg"]:
                images += glob.glob(os.path.join(IMAGES_FOLDER, t))

            log(f"Images found: {len(images)}")

            if not images:
                log(f"ERROR: No images in {IMAGES_FOLDER}")
                log("Please put images in the incoming folder!")
                with open(RESULT_FILE, "w") as f:
                    f.write("No Image Found")
            else:
                # detect front and rear damage
                log('start moving new images from source to destination')
                car_license_numebr = '1' # TODO: will replace with plate detection
                # patterns for get image name and ext
                pattern = r'([^\\/]+)\.(png|jpg)'
                log(f'{images}')

                # read license number
                with open(PLATE_NUMBER_RESULT, "r") as f:
                    license_number = f.read().strip()  
                # remove folder if exist
                recreate_folder(os.path.join(DESTINATION_FOLDER, license_number))
                log('recreated the destination folder')

                for image in images:
                    log(f'saving {image}')
                    matches = re.findall(pattern, image)
                    print(matches)
                    image = matches[0][0] +'.'+ matches[0][1] 
                    source_path = os.path.join(IMAGES_FOLDER, image)
                    image = license_number + '\\' + image # add destination folder
                    destination_path = os.path.join(DESTINATION_FOLDER, image)
                    os.rename(source_path, destination_path)

                    log(f'{image} saved!')

                with open(RESULT_FILE, "w") as f:
                    f.write("images moved")                    


        except Exception as e:
            log(f"ERROR: {type(e).__name__}: {e}")
            with open(RESULT_FILE, "w") as f:
                f.write("Error")

    time.sleep(0.1)

log("Stop flag detected. Worker exiting cleanly.")