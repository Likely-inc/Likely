from random import randint
import time


SEP = "."
class LikesHandler:
    __img = None
    __text = None
    __currTime = time.localtime()

    def LikesHandler(self, img, text):
        __img = img
        __text = text
        l = self.generateTimeFrames(self.__currTime)


    def generateTimeFrames(self, cClock):
        l = []
        data = cClock[0] + SEP + cClock[1] + SEP + cClock[2]
        currTime = int(cClock[3])
        while(currTime!=0):
            l.append(data+SEP+str(currTime))
            currTime-=1






