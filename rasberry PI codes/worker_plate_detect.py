import time
import os
import glob




# set log function
def log(msg, LOG_FILE):
    timestamp = time.strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def check_reqs(LOG_FILE, IMAGES_FOLDER, PLATE_NUMBER_RESULT):
   # check file writing
   try:
       with open(LOG_FILE, "w") as f:
            f.write("=== Worker started ===\n")
   except Exception as e:
       return "ERR(WPD):-log can't reach"

   log("Step 1 OK: Logging works.", LOG_FILE)

   # check file/folder paths
   log(f"Step 2: Checking paths...", LOG_FILE)
   log(f"  IMAGES_FOLDER exists:  {os.path.exists(IMAGES_FOLDER)}", LOG_FILE)
   log(f"  IMAGES_FOLDER exists:  {os.path.exists(PLATE_NUMBER_RESULT)}", LOG_FILE)

   os.makedirs(IMAGES_FOLDER, exist_ok=True)

   log("Step 3 OK: Folders ready.", LOG_FILE)

   # main loop of worker
   log("Step 4: Entering main loop...", LOG_FILE)
   

def detect_plate(LOG_FILE, IMAGES_FOLDER, PLATE_NUMBER_RESULT, plate_number = '0'):
        # check system reqs
    check_reqs(LOG_FILE, IMAGES_FOLDER, PLATE_NUMBER_RESULT)

    log("Looking for images...", LOG_FILE)
    
    try:
        images = []
        for t in ["*.png", "*.jpg", "*.jpeg"]:
            images += glob.glob(os.path.join(IMAGES_FOLDER, t))

        log(f"Images found: {len(images)}", LOG_FILE)

        if not images:
            log(f"ERROR: No images in {IMAGES_FOLDER}", LOG_FILE)
            return "ERR(WPD):-No image!"
    
        else:
            image_path = [imgpth for imgpth in images if "front" in imgpth][0]
            log(f"detect: {os.path.basename(image_path)}", LOG_FILE)

            # TODO: will send to license detection

            with open(PLATE_NUMBER_RESULT, "w") as f:
                f.write(plate_number)
        
            log("licence number written", LOG_FILE)
            return "OK"

    except Exception as e:
        return "ERR(WPD):-check func"
