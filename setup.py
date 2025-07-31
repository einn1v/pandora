import os
import time

print("You are currently installing PanDoRa. You will first need to install the required dependencies. Do you want to continue?\n[y/n]")
if input().lower() == "y":
    os.system("pip install -r requirements.txt")
    print("Dependencies installed successfully.")
    input()
else:
    print("Installation cancelled.")
    time.sleep(1)
    exit(0)