import time
import os

p = os.listdir("upload")
for d in os.listdir("upload"):
    for elem in os.listdir(d):
        print(elem)