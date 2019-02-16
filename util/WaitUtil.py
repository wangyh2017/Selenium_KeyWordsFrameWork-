#encoding=utf-8
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC

class WaitUtil(object):
    def __init__(self,driver):
        self.locationTypeDict={
            "xpath":By.XPATH,
            "id":By.ID,
            "name":By.NAME,
            "class_name":By.TAG_NAME,
            "link_text":By.LINK_TEXT,
            "partical_link_text":By.PARTIAL_LINK_TEXT
        }

        self.driver = driver
        self.wait = WebDriverWait(self.driver,30)

    def presenceOfElementLocated(self, locatorMethod, locatorExpression,*args):
        # 显示等待页面元素出现在DOM中，但并一定可见，存在则返回该页面元素对象

        try:
            if self.locationTypeDict.has_key((locatorMethod.lower())):
                self.wait.until(
                    EC.presence_of_all_elements_located
                            ((self.locationTypeDict[locatorMethod.lower()], locatorExpression)))
            else:
                raise  TypeError(u"未找到定位方式，请确认定位方法是否正确")
        except Exception,e:
            #抛出异常给上层调用者
            raise e


    def frameToBeAvailableAndSwitchToIt(self,locationType,locatorExpression,*arg):
        #检查frame是否存在，存在则切换到frame空控件中
        try:
            self.wait.until(
                EC.frame_to_be_available_and_switch_to_it((
                    self.locationTypeDict[locationType.lower()],
                    locatorExpression
                )))
        except Exception,e:
            #抛出异常给上层调用者
            raise e

    def visibilityOfElementLocated(self,locationType,locatorExpression,*arg):
        #显示等待页面元素出现在DOM中，并且可见，存在则返回该页面元素对象
        try:
            self.wait.until(
                EC.visibility_of_element_located((
                    self.locationTypeDict[locationType.lower()],
                    locatorExpression
                )))
        except Exception,e:
            #抛出异常给上层调用者
            raise e


if __name__ == '__main__':
    from selenium import webdriver
    driver = webdriver.Chrome(executable_path="/Users/wangyanhua/Documents/学习/Python/webdrive/chromedriver")
    driver.get("http://mail.126.com")
    waitUtil = WaitUtil(driver)
    #waitUtil.frame_available_and_switch_to_it("id","x - URS - iframe")  #检查框架的代码更换
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    waitUtil.visibilityOfElementLocated("xpath","//input[@name='email']")
    waitUtil.presenceOfElementLocated("xpath","//input[@name='email']")
    driver.quit()
