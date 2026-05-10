import time
import os

STOP_FILE      = r"E:\files\my projects\car_damage_system\data\stop.flag"
RESULT_FILE    = r"E:\files\my projects\car_damage_system\data\result.txt"
NEW_IMAGE_FLAG = r"E:\files\my projects\car_damage_system\data\new_image.flag"
LOG_FILE       = r"E:\files\my projects\car_damage_system\data\worker_log.txt"
IMAGES_FOLDER  = r"E:\files\my projects\car_damage_system\data\images"
PLATE_NUMBER_RESULT = r"E:\files\my projects\car_damage_system\data\detect_car_worker_plate_number.txt"
INC_IMAGES_FOLDER  = r"E:\files\my projects\car_damage_system\incoming"
SERVER_URL     = "http://127.0.0.1:5000/predict"

# check file writing
try:
    with open(LOG_FILE, "w") as f:
        f.write("=== Worker started ===\n")
except Exception as e:
    import sys
    sys.exit(f"FATAL: Cannot write log: {e}")

with open(PLATE_NUMBER_RESULT, 'r') as f:
    result = f.read().strip()
    IMAGES_FOLDER = os.path.join(IMAGES_FOLDER, result)

# set logs for reading new images
def log(msg):
    timestamp = time.strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

log("Step 1 OK: Logging works.")

# check requests
log("Step 2: Importing requests...")
try:
    import requests
    log("Step 2 OK: requests imported.")
except Exception as e:
    log(f"Step 2 FAILED: {e}")

log("Step 3: Importing glob...")
try:
    import glob
    log("Step 3 OK: glob imported.")
except Exception as e:
    log(f"Step 3 FAILED: {e}")

# check file/folder paths
log(f"Step 4: Checking paths...")
log(f"  STOP_FILE exists:      {os.path.exists(STOP_FILE)}")
log(f"  NEW_IMAGE_FLAG exists: {os.path.exists(NEW_IMAGE_FLAG)}")
log(f"  IMAGES_FOLDER exists:  {os.path.exists(IMAGES_FOLDER)}")

log("Step 4 OK: Folders ready.")

# check server
log("Step 5: Testing server connection...")
try:
    import requests as req
    r = req.get("http://127.0.0.1:5000/", timeout=3)
    log(f"Step 5 OK: Server reachable. Status: {r.status_code}")
except Exception as e:
    log(f"Step 5 FAILED: Server not reachable: {e}")
    log("WARNING: Will keep trying in main loop...")

# main loop of worker
log("Step 6: Entering main loop...")
loop_count = 0

def read_images(path):
    images = []
    for t in ["*.png", "*.jpg", "*.jpeg"]:
        images += glob.glob(os.path.join(path, t))

    log(f"{path} Images found: {len(images)}")
    return images

def img_proc(images):   
    details = dict()
    for place in ['rear', 'front']:
        image_path = [imgpth for imgpth in images if place in imgpth][0]
        log(f'{image_path}')
        log(f"Processing: {os.path.basename(image_path)}")

        with open(image_path, "rb") as f:
            response = requests.post(
                SERVER_URL,
                files={"image": f},
                timeout=5
            )
        result = response.json()["result"]
        log(f"Result: {result}")
        details[place] = result
    return details
        

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
            images = read_images(IMAGES_FOLDER)
            income = read_images(INC_IMAGES_FOLDER)

            if not images:
                log(f"ERROR: No images in {IMAGES_FOLDER}")
                log("Please put images in the incoming folder!")
                with open(RESULT_FILE, "w") as f:
                    f.write("No Image Found")
            else:
                # detect front and rear damage
                saved = img_proc(images)
                income = img_proc(income)
                result = ''
                if saved['rear'] != income['rear']:
                    result += income['rear']
                else:
                    result += 'Rear Normal'
                
                result += '\n'

                if saved['front'] != income['front']:
                    result += income['front']
                else:
                    result += 'Front Normal'

                with open(RESULT_FILE, "w") as f:
                    f.write(result)
                log("Result written OK.")
        # error handlers
        except requests.exceptions.ConnectionError:
            log("ERROR: Inference server not running!")
            with open(RESULT_FILE, "w") as f:
                f.write("Server Error")
        except Exception as e:
            log(f"ERROR: {type(e).__name__}: {e}")
            with open(RESULT_FILE, "w") as f:
                f.write("Error")

    time.sleep(0.1)

log("Stop flag detected. Worker exiting cleanly.")