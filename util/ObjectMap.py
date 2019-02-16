#encoding=utf-8
from selenium.webdriver.support.ui import WebDriverWait

#获取单个页面元素对象
def getElement(driver,locationType,locatorExpression):
    try:
        element = WebDriverWait(driver,30).until(lambda x:x.find_element(by=locationType,value=locatorExpression))
        return  element
    except Exception,e:
        raise e

#获取读个页面元素对象,以list返回
def getElements(driver,locationType,locatorExpression):
    try:
        elements = WebDriverWait(driver,30).until(lambda x:x.find_elements(by=locationType,value=locatorExpression))
        return elements
    except Exception,e:
        raise e

if __name__ =='__main__':
    from selenium import webdriver
    #进行单元测试
    driver = webdriver.Firefox(executable_path="/Users/wangyanhua/Documents/学习/Python/webdrive/geckodriver")
    driver.get("http://www.baidu.com")
    searchBox = getElement(driver,"id","kw")
    print searchBox.tag_name
    #打印页面对象的签名
    aList = getElements(driver,"tag name","a")
    print len(aList)
    driver.quit()




#执行结果：
""" 
/usr/bin/python /Users/wangyanhua/Documents/学习/Python/sele_frame/chapt_15/KeyWordsFrameWork/util/ObjectMap.py
'import sitecustomize' failed; use -v for traceback
input
33
"""