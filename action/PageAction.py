#encoding=utf-8
from selenium import  webdriver
from chapt_15.KeyWordsFrameWork.config.VarConfig import chromeDriverFilePath
from chapt_15.KeyWordsFrameWork.config.VarConfig import firefoxDriverFilePath
from chapt_15.KeyWordsFrameWork.config.VarConfig import ieDriverFilePath
from chapt_15.KeyWordsFrameWork.util.ClipboardUtil import Clipboard
from chapt_15.KeyWordsFrameWork.util.ObjectMap import getElement
from chapt_15.KeyWordsFrameWork.util.keyBoardUtil import KeyboardKeys
from chapt_15.KeyWordsFrameWork.util.DirAndTime import *
from chapt_15.KeyWordsFrameWork.util.WaitUtil import WaitUtil
from selenium.webdriver.chrome.options import  Options
import time
from selenium.webdriver import  ActionChains
from  selenium.webdriver.common.keys import Keys

"""具体页面动作"""

#定义全局driver变量
driver = None
#全部的等待类实例对象
waitUtil = None

def open_browser(browserName,*arg):
    #打开浏览器
    global driver,waitUtil
    try:
        if browserName.lower() == 'firefox':
            driver = webdriver.Firefox(executable_path=firefoxDriverFilePath)

        elif browserName.lower() == 'chrome':
            #创建Chrome浏览器的一个options实例对象
            chrome_option = Options()
            #添加屏蔽--ignore-certificate-errors 提示信息的设置参数项
            chrome_option.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
            driver = webdriver.Chrome(
                executable_path= chromeDriverFilePath,
                chrome_options=chrome_option
            )
        else:
            driver=webdriver.Ie(executable_path=ieDriverFilePath)
            #driver 对象创建成果后，创建等待类实例对象
            waitUtil = WaitUtil(driver)
    except Exception,e:
        raise e

def visit_url(url,*arg):
    #访问某个网址
    global  driver
    try:
        driver.get(url)
    except Exception,e:
        raise e

def close_browser(*arg):
    #关闭浏览器
    global driver
    try:
        driver.quite()
    except Exception,e:
        raise  e

def sleep(sleepSeconds,*arg):
    #强制等待
    try:
        time.sleep(int(sleepSeconds))
    except Exception,e:
        raise e

def clear(locationType,locatorExpression,*arg):
    #清除输入框默认内容
    global driver
    try:
        getElement(driver,locationType,locatorExpression).clear()
    except Exception,e:
        raise e

def input_string(locationType,locatorExpression,inputContent):
    #在页面上输入框中输入数据
    global driver
    try:
        getElement(driver,locationType,locatorExpression).send_keys(inputContent)

    except Exception,e:
        raise  e

def click(locationType,locatorExpression,*arg):
    #单击页面元素
    global driver
    try:
        getElement(driver,locationType,locatorExpression).click()
    except Exception,e:
        raise  e

def assert_string_in_pagesource(assertString,*arg):
    #断言页面源码是否存在某关键字或关键字符串
    global driver
    try:
        assert  assertString in driver.page_source, u"%s not found in page source!" %assertString

    except  AssertionError,e:
        raise AssertionError(e)
    except Exception,e:
        raise e
def assert_title(titleStr,*args):
    #断言页面标题是否存在给定的关键字符串
    global driver
    try:
        assert titleStr in driver.title, u"%s not found in title!" % titleStr
    except  AssertionError,e:
        raise AssertionError(e)
    except Exception,e:
        raise e


def getTitle(*arg):
    #获取页面标题
    global  driver
    try:
        return  driver.title
    except Exception,e:
        raise e

def getPageSorce(*arg):
    #获取页面源码
    global  driver
    try:
        return  driver.page_source
    except Exception,e:
        raise e

def switch_to_frame(locationType,locatorExpression,*arg):
    #切换进入到frame
    global driver
    try:
        driver.switch_to.frame(getElement(driver,locationType,locatorExpression))
    except Exception,e:
        print "frame error"
        raise e

def switch_to_default_content(*arg):
    #切出frame
    global  driver
    try:
        driver.switch_to.default_content()
    except Exception,e:
        raise  e

def paste_string(pasteString,*arg):
    #模拟Ctrl +V
    try:
        Clipboard.setClipboardData(pasteString)
        #等待两秒，防止代码执行的太快，而未成功黏贴内容
        time.sleep(2)
        ActionChains(driver).key_down(Keys.COMMAND).send_keys("v").key_up(Keys.COMMAND).perform()
    except Exception,e:
        raise  e

def press_tab_key(*arg):
    #模拟tab键
    try:
        ActionChains(driver).key_down(Keys.TAB)
    except Exception,e:
        raise e

def press_enter_key(*arg):
    #模拟enter键
    try:
        ActionChains(driver).key_down(Keys.RETURN)
    except Exception,e:
        raise e

def maximize_browser():
    #窗口最大化
    global driver
    try:
        driver.maximize_window()
    except Exception,e:
        raise  e

def capture_screen(*args):
    #获取屏幕截图
    global  driver
    currTime = getCurrentTime()
    print currTime
    picNameAndPath = str(createCurrentDataDir()) +"/" + str(currTime) +".png"
    try:
        driver.get_screenshot_as_file(picNameAndPath.replace('/',r'/'))
    except Exception,e:
        raise  e


def waitPresenceOfElementLocated(locationType,locatorExpression,*arg):
    #显示等待页面元素出现在DOM中，但并不一定可见，存在则返回该页面元素对象

    global waitUtil
    try:
        waitUtil.presenceOfElementLocated(locationType,locatorExpression)
    except Exception,e:
        raise e
def waitFrameToBeAviailableAndSwitchToIt(locationType,locatorExpression,*args):
    #检查frame是否存在，存在则切换进frame控件中
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    """ 
    global waitUtil
    try:
        waitUtil.frameToBeAvailableAndSwitchToIt(locationType,locatorExpression)
    except Exception,e:
        raise e
    """

def waitVisibilityOfElementLocated(locationType,locatorExpression,*args):
    wait = WaitUtil(driver)
    driver.switch_to.default_content()  # 添加的代码
    element = wait.frameToBeAvailableAndSwitchToIt("xpath","//span[text()='写 信']")
    element.click()
    #显示等待页面元素出现在DOM中，并且可见，存在则返回该页面元素对象
    global  waitUtil
    try:
        waitUtil.visibilityOfElementLocated(locationType,locatorExpression)
    except Exception,e:
        raise e













