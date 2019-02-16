#encoding=utf-8
#encoding=utf-8
#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from selenium import webdriver
import unittest
import time
from pymouse import PyMouse
from pykeyboard import PyKeyboard
#导入支持双击事件的包，双击，悬浮，拖拽等
from selenium.webdriver import  ActionChains
#导入select模块
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import subprocess  #子进程
class Clipboard(object):
    """模拟Windows设置剪贴板"""

    # 设置和读取剪切板：
    #读取剪切版
    @staticmethod
    def getClipboardData():
        p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
        retcode = p.wait()
        data = p.stdout.read()
        # 这里的data为bytes类型，之后需要转成utf-8操作
        return data


    # 设置剪切板内容
    @staticmethod
    def setClipboardData(data):
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        p.stdin.write(data)
        p.stdin.close()
        p.communicate()


