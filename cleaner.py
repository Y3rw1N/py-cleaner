#!/data/data/com.termux/files/usr/bin/python3

import os
from time import sleep
import datetime 
import threading
import shutil
import glob

ANDROID_APPS_TMP_DIRS = [
    "/data/data/*/cache/*",
    "/data/data/*/code_cache/*",
    "/data/user_de/*/*/cache/*",
    "/data/user_de/*/*/code_cache/*",
    "/sdcard/Android/data/*/cache/*"
]

def count_temp_files():
    count = 0
    for paths in ANDROID_APPS_TMP_DIRS:
        count += len(glob.glob(paths))
    return count

date = datetime.datetime.now().strftime("%d-%m-%y %H:%M")

def anim(exc):
    while exc.is_alive():
        for dots in ["", ".", "..", "..."]:
            print(f"\rCleaning apps{dots}", end="")
            sleep(0.3)
        print("\rCleaning apps... done", end="")


def log(message):
    log_dir = "/sdcard/pycleaner"
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "log.txt"), "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")


def cleaner():
    for paths in ANDROID_APPS_TMP_DIRS:
        for temp_path in glob.glob(paths):
            try:
                if os.path.isfile(temp_path):
                    os.remove(temp_path)
                    log(f"{date} deleting {temp_path}")
                else:
                    shutil.rmtree(temp_path)
                    log(f"{date} deleting {temp_path}")
            except Exception as e:
                log(f"{date} [ERROR]: there was a problem trying to delete a file or directory: {e}")


if __name__ == "__main__":
   if os.geteuid() != 0:
    print("root only >:C")
    exit(1)

   if count_temp_files() == 0:
    print("[\033[33m!\033[0m] No temporary files to clean. Exiting.")
    exit(0)
    
   thread_cleaner = threading.Thread(target=cleaner)
   thread_anim = threading.Thread(target=anim, args=(thread_cleaner,))

   thread_cleaner.start()
   thread_anim.start()
   
   thread_cleaner.join()
   thread_anim.join()
