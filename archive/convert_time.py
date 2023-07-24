def convertTime (time):
    temp = time.split(':')
    timeMinutes = (int(temp[0])*60)+int(temp[1])+int(temp[2])/60
    return timeMinutes