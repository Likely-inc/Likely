import time
import os, os.path

for root, _, files in os.walk("upload"):
    for f in files:
        fullpath = os.path.join(root, f)
        print(fullpath)
        print(os.path.getmtime(fullpath)/60/60)