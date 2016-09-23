def parseResults(l):
    l.sort(key=lambda x: x[1], reverse=True)
    newL = []
    maxV = l[0][1]
    for elem in l:
        newL.append((elem[0], elem[1], int((elem[1] / maxV)*100)))
    newL.sort(key=lambda x: int(x[0]))
    return newL



statuses = [("1",10),("2",15),("3",11),("4",29),("5",12),("6",10),("7",35),("8",30),("9",32),("10",30)]
print(parseResults(statuses))