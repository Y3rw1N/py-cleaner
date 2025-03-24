#!/data/data/com.termux/files/usr/bin/python3

import os
from time import sleep
import subprocess
import datetime 
import threading
import shutil
import glob

ANDROID_APPS_TMP_DIRS = [
    "/storage/emulated/0/Android/data/*/cache/*",
    "/data/data/*/cache/*",
    "/data/data/*/code_cache/*",
    "/data/user_de/0/*/cache/*",
    "/data/user_de/0/*/code_cache/*",
    "/data_mirror/data_de/null/0/*/cache/*",
    "/data_mirror/data_de/null/0/*/code_cache/*",
    "/data_mirror/data_ce/null/0/*/cache/*",
    "/data_mirror/data_ce/null/0/*/code_cache/*"
]

date = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")

def android_api_level():
    try:
        result = subprocess.check_output(["getprop", "ro.build.version.sdk"]).strip()
        return int(result)
    except Exception as e:
        print(f"[Error]: {e}")
        return -1

def anim(exc):
    while exc.is_alive():
        for dots in ["", ".", "..", "..."]:
            print(f"\rCleaning apps{dots}", end="")
            sleep(0.3)
        print("\rCleaning apps... done", end="")


def log(message):
    log_dir = "/sdcard/pycleaner"
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, f"{date}-log.txt"), "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")

def cleaner():
    for paths in ANDROID_APPS_TMP_DIRS:
        for temp_path in glob.glob(paths):
            try:
                if os.path.isfile(temp_path):
                    os.remove(temp_path)
                    log(f"deleting {temp_path}")
                else:
                    shutil.rmtree(temp_path)
                    log(f"deleting {temp_path}")
            except Exception as e:
                log(f"{date} [ERROR]: there was a problem trying to delete a file or directory: {e}")


if __name__ == "__main__":
   if os.geteuid() != 0:
    print("root only >:C")
    exit(1)

   if android_api_level() < 21:
        print("[\033[31m!\033[0m] you need android 5 or higher (API 21+)  ")

   thread_cleaner = threading.Thread(target=cleaner)
   thread_anim = threading.Thread(target=anim, args=(thread_cleaner,))

   thread_cleaner.start()
   thread_anim.start()
   
   thread_cleaner.join()
   thread_anim.join()
