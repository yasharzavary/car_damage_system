import time
import os

STOP_FILE      = r"E:\files\my projects\car_damage_system\data\stop.flag"
RESULT_FILE    = r"E:\files\my projects\car_damage_system\data\save_image_result.txt"
NEW_IMAGE_FLAG = r"E:\files\my projects\car_damage_system\data\detect_car_new_image.flag"
LOG_FILE       = r"E:\files\my projects\car_damage_system\data\detect_car_worker_log.txt"
IMAGES_FOLDER  = r"E:\files\my projects\car_damage_system\incoming"
PLATE_NUMBER_RESULT = r"E:\files\my projects\car_damage_system\data\detect_car_worker_plate_number.txt"

# check file writing
try:
    with open(LOG_FILE, "w") as f:
        f.write("=== Worker started ===\n")
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
                image_path = [imgpth for imgpth in images if "front" in imgpth][0]
                log(f'{image_path}')
                log(f"detect: {os.path.basename(image_path)}")

                # TODO: will send to license detection
                result = '2' # for now always 1

                with open(RESULT_FILE, "w") as f:
                    f.write('licence detected!')

                with open(PLATE_NUMBER_RESULT, "w") as f:
                    f.write(result)
                log("licence number written OK.")

        except Exception as e:
            log(f"ERROR: {type(e).__name__}: {e}")
            with open(RESULT_FILE, "w") as f:
                f.write("Error")

    time.sleep(0.1)

log("Stop flag detected. Worker exiting cleanly.")