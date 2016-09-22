import time
import os

p = os.listdir("upload")
for d in os.listdir("upload"):
    if(os.path.isfile(d)):
        print(d)
        print("Is file!!")
    elif(os.path.isdir(d)):
        print(d)
        print("Is dir!!")
        for elem in os.listdir(d):
            print(d)
            print("Is file!!")

