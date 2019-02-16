#encoding=utf-8
import time,os
from datetime import datetime
from chapt_15.KeyWordsFrameWork.config.VarConfig import  screenPicturesDir

#获取当前日期：
def getCurrentData():
    timeTup = time.localtime()
    currentData = str(timeTup.tm_year) + "-" + str(timeTup.tm_mon) + "-" + str(timeTup.tm_mday)
    return  currentData

#获取当前时间
def getCurrentTime():
    timeStr = datetime.now()
    nowTime = timeStr.strftime('%H-%M-%S-%f')
    return  nowTime

#创建截图保存路径
def createCurrentDataDir():
    dirName = os.path.join(screenPicturesDir,getCurrentData())
    if not os.path.exists(dirName):
        os.makedirs(dirName)

    return  dirName

if __name__ == '__main__':
    print getCurrentData()
    print u"createCurrentDataDir地址：",createCurrentDataDir()
    print u"getCurren为：",getCurrentTime()


