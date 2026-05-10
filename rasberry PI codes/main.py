import RPi.GPIO as GPIO
import time
import os
import sys
import subprocess
import traceback

import worker_plate_detect as wpd
import worker_save_image as wsi

# pin definition
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

SIGNAL_PIN = 15          # LogicState input

# LCD pins (4-bit mode)
LCD_RS = 26
LCD_E  = 24
LCD_D4 = 22
LCD_D5 = 18
LCD_D6 = 16
LCD_D7 = 13

# buzzer settings
BUZZER = 12

# ultrasonic sensors
CAR_OUT_PIR = 29
CAR_IN_PIR = 31




# LCD pins
LCD_WIDTH = 16
LCD_CHR   = True
LCD_CMD   = False
LCD_LINE1 = 0x80
LCD_LINE2 = 0xC0

GPIO.setup(SIGNAL_PIN, GPIO.IN)
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_E,  GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)	

GPIO.setup(BUZZER, GPIO.OUT)

# car detection
GPIO.setup(CAR_OUT_PIR, GPIO.IN)
GPIO.setup(CAR_IN_PIR, GPIO.IN)

# paths
STOP_FILE      = r"E:\files\my projects\car_damage_system\data\stop.flag"
RESULT_FILE    = r"E:\files\my projects\car_damage_system\data\result.txt"
NEW_IMAGE_FLAG = r"E:\files\my projects\car_damage_system\data\new_image.flag"
WORKER_CAR_DETECTION_PATH = r"E:\files\my projects\car_damage_system\worker_damage_detection.py"
CRASH_LOG      = r"E:\files\my projects\car_damage_system\data\worker_crash.txt"
REAL_PYTHON    = r"C:\Users\Windows\AppData\Local\Programs\Python\Python310\python.exe"

os.makedirs(r"E:\files\my projects\car_damage_system\data", exist_ok=True)

# all functions need
IMAGES_FOLDER  = r"E:\files\my projects\car_damage_system\incoming"
PLATE_NUMBER_RESULT = r"E:\files\my projects\car_damage_system\data\detect_car_worker_plate_number.txt"
DESTINATION_FOLDER = r"E:\files\my projects\car_damage_system\data\images"

# wpd
WPD_LOG_FILE       = r"E:\files\my projects\car_damage_system\data\detect_car_worker_log.txt"

# wsi
WSI_LOG_FILE       = r"E:\files\my projects\car_damage_system\data\worker_save_image_log.txt"


# Functions
# LCD functions
def lcd_toggle_enable():
    time.sleep(0.0005)
    GPIO.output(LCD_E, True)
    time.sleep(0.0005)
    GPIO.output(LCD_E, False)
    time.sleep(0.0005)
    
def lcd_byte(bits, mode):
    GPIO.output(LCD_RS, mode)
    # High nibble
    GPIO.output(LCD_D4, bool(bits & 0x10))
    GPIO.output(LCD_D5, bool(bits & 0x20))
    GPIO.output(LCD_D6, bool(bits & 0x40))
    GPIO.output(LCD_D7, bool(bits & 0x80))
    lcd_toggle_enable()
    # Low nibble
    GPIO.output(LCD_D4, bool(bits & 0x01))
    GPIO.output(LCD_D5, bool(bits & 0x02))
    GPIO.output(LCD_D6, bool(bits & 0x04))
    GPIO.output(LCD_D7, bool(bits & 0x08))
    lcd_toggle_enable()

def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)  # 4-bit, 2 line
    lcd_byte(0x0C, LCD_CMD)  # display on, cursor off
    lcd_byte(0x06, LCD_CMD)  # entry mode
    lcd_byte(0x01, LCD_CMD)  # clear display
    time.sleep(0.002)

# text decoder for LCD    
def lcd_show(line1, line2=""):
    """Display two lines on LCD."""
    # Line 1
    lcd_byte(LCD_LINE1, LCD_CMD)
    text1 = line1.ljust(LCD_WIDTH)[:LCD_WIDTH]
    for char in text1:
        lcd_byte(ord(char), LCD_CHR)
    # Line 2
    lcd_byte(LCD_LINE2, LCD_CMD)
    text2 = line2.ljust(LCD_WIDTH)[:LCD_WIDTH]
    for char in text2:
        lcd_byte(ord(char), LCD_CHR)
    print(f"[LCD] {line1.strip()} | {line2.strip()}")
      

      
def default_settings():
    # clean up
    for f in [STOP_FILE, NEW_IMAGE_FLAG, RESULT_FILE]:
        if os.path.exists(f):
            os.remove(f)

    # enable LCD
    lcd_init()
    lcd_show("System Ready", "Waiting...")
    print("[Main] LCD initialized.")

    #  run worker for damage detection
    crash_log_file = open(CRASH_LOG, "w")
    proc_damage_detect_worker = subprocess.Popen(
        [REAL_PYTHON, WORKER_CAR_DETECTION_PATH],
        stdout=crash_log_file,
        stderr=crash_log_file,
        text=True
    )
    print(f"[Main] Damage Detection Worker launched. PID: {proc_damage_detect_worker.pid}")
    time.sleep(2)
    return proc_damage_detect_worker, crash_log_file

def check_systems(proc):
    # check worker
    if proc.poll() is not None:
        print(f"[Main] ERROR: Worker died! Check worker_crash.txt")
    else:
        print(f"[Main] Worker running OK.")
        lcd_show("Worker Ready", "Send signal...")

def check_car(dir):
    return GPIO.input(CAR_OUT_PIR if dir == 'out' else CAR_IN_PIR)

def car_out_procedure():
    # notify the User and set flag
    print("[Main] Car detected! Notifying worker...")
    lcd_show("New Image!", "Processing...")
    with open(NEW_IMAGE_FLAG, "w") as f:
        f.write("new")
    
    front_damage = ''
    rear_damage = ''
    while not os.path.exists(STOP_FILE):
        if os.path.exists(RESULT_FILE):
            with open(RESULT_FILE, "r") as f:
                result = f.read().strip()
            if result == "Server Error":
                lcd_show("Server Error!", "Check Server")
                raise RuntimeError("Server Error!")
            print(f"[Main] Result: {result}")
        
            rear_damage, front_damage = result.split('\n')

            front_damage = front_damage[:16]
            rear_damage = rear_damage[:16]
            if "Normal" not in rear_damage or "Normal" not in front_damage:
                GPIO.output(BUZZER, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(BUZZER, GPIO.LOW) 

            lcd_show(front_damage, rear_damage)
            if os.path.exists(RESULT_FILE):
                os.remove(RESULT_FILE)
            print("[Main] Ready for next car.")
            return

        time.sleep(0.1)                      


# default settings
proc_damage_detect_worker, crash_log_file = default_settings()
# check workers
check_systems(proc_damage_detect_worker)

# state tracking
last_result    = None
waiting_result = 0
show_lcd = False
dd_same_car = False
si_same_car = False
start_detection = False

print("[Main] Monitoring OUT camera for new signal...")

try:
    while not os.path.exists(STOP_FILE):
        # set and ensure everything is OK!

        # check out car
        car_out_pir_signal = check_car('out')
        car_in_pir_signal = check_car('in')
    
        if car_out_pir_signal and car_in_pir_signal:
            pass # TODO: we will create a circuit to announce that both line is stuck

        # out car detection control section
        if car_out_pir_signal and not dd_same_car:
            wpd.detect_plate(WPD_LOG_FILE, IMAGES_FOLDER, PLATE_NUMBER_RESULT)
            time.sleep(0.02)
            car_out_procedure()
            dd_same_car = True
        elif not car_out_pir_signal and dd_same_car:
            dd_same_car = False

        # in car detection control section
        if car_in_pir_signal and not si_same_car:
            wpd_result = wpd.detect_plate(WPD_LOG_FILE, IMAGES_FOLDER, PLATE_NUMBER_RESULT)
            if 'ERR' in wpd_result:
                line1, line2 = wpd_result.split('-')
                lcd_show(line1, line2)
                time.sleep(2)
                continue
            time.sleep(0.02)
            wsi_result = wsi.save_image(WSI_LOG_FILE, IMAGES_FOLDER, DESTINATION_FOLDER, PLATE_NUMBER_RESULT)
            if 'ERR' in wsi_result:
                line1, line2 = wsi_result.split('-')
                lcd_show(line1, line2)
                time.sleep(2)
                continue
            lcd_show('Wellcome!', "    ^---^")
            si_same_car = True
        elif not car_in_pir_signal and si_same_car:
            si_same_car = False
    
        time.sleep(0.02)

except Exception as e:
    print(f"[Main] EXCEPTION: {type(e).__name__}: {e}")
    traceback.print_exc()

finally:
    with open(STOP_FILE, "w") as f:
        f.write("stop")
    proc_damage_detect_worker.kill()
    crash_log_file.close()
    lcd_show("System Stopped", "")
    GPIO.cleanup()
    print("[Main] Stopped cleanly.")
    os._exit(0)