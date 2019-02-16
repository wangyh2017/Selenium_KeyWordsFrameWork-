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


class KeyboardKeys(object):
    """模拟键盘操作"""
    VK_CODE={

    }
