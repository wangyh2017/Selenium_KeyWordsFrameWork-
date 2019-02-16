#encoding=utf-8
from  chapt_15.KeyWordsFrameWork.util.ObjectMap import *
from  chapt_15.KeyWordsFrameWork.util.keyBoardUtil import KeyboardKeys
from  chapt_15.KeyWordsFrameWork.util.ClipboardUtil  import Clipboard
from  chapt_15.KeyWordsFrameWork.util.WaitUtil  import  WaitUtil
from  selenium import  webdriver
from  selenium.webdriver.common.keys import Keys
from selenium.webdriver import  ActionChains
from chapt_15.KeyWordsFrameWork.action.PageAction import *
from chapt_15.KeyWordsFrameWork.util.ParseExcel import ParseExcel
from chapt_15.KeyWordsFrameWork.config.VarConfig import *
import time
import  traceback
#设置此次环境的编码为utf-8
import  sys
reload(sys)
sys.setdefaultencoding("utf-8")
import sys

#创建解析Excel对象
excelObj = ParseExcel()
#将Excel数据文件加载到内存
excelObj.loadWorkBook(dataFilePath)  #获取不到

#用例或用例步骤执行结束后，向Excel中写执行结果信息
def writeTestResult(sheetObj,rowNo,colNo,testResult,errorInfo=None,picPath = None):
    #测试通过结果为绿色，失败为红色
    colorDict = {"pass":"green","failed":"red"}

    #因为测试用例工作表和用例步骤工作表都有执行时间和测试结果列，定义此字典对象是为了区分具体应该写那个工作表
    colorDict = {
        "testCase":[testCase_runTime,testCase_testResult],
        "caseStep":[testStep_runTime,testStep_testResult]
    }
    try:
        #在测试步骤sheet中写入测试时间
        excelObj.writeCellCurrentTime(sheetObj,rowNo=rowNo,colsNo=colorDict[colNo][0])

        #在测试步骤sheet表中，写入测试结果
        excelObj.writeCell(sheetObj,content=testResult,
                           rowNo=rowNo,colsNo=colorDict[colNo][1],
                           style=colorDict[testResult])
        if errorInfo and picPath:
            #在测试步骤sheet中，写入异常信息
            excelObj.writeCell(sheetObj,content=errorInfo,
                               rowNo=rowNo,colsNo=testStep_errorInfo)
            #在测试步骤sheet中，写入写入异常截图路径
            excelObj.writeCell(sheetObj,content=picPath,
                               rowNo=rowNo,colsNo=testStep_errorPic)
        else:
            #在测试步骤sheet中，清空异常信息单元格
            excelObj.writeCell(sheetObj,content="",
                               rowNo=rowNo,colsNo=testStep_errorInfo)
            excelObj.writeCell(sheetObj,content="",
                               rowNo=rowNo,colsNo=testStep_errorPic)
    except Exception,e:
        print u"写excel出错",traceback.print_exc()


def TestSendMailWithAttachment():
    try:
        #根据Excel文件中的sheet表名获取sheet对象
        caseSheet = excelObj.getSheetByName(u"测试用例")
        #获取测试用例sheet中是否执行列对象
        isExecuteColumn = excelObj.getColumn(caseSheet, testCase_isExecute)
        #记录成功执行成功的测试用例个数
        successfulCase = 0
        #记录需要执行的用例个数
        requireCase = 0
        for idx,i in enumerate(isExecuteColumn[1:]):
            #因为用例sheet中的第一行为标题行，无需执行
            #print i.value
            #循环遍历"测试用例"表中的测试用例，执行被设置为执行的用例
            # 表示要执行
             if i.value.lower() == "y":
                requireCase +=1
                #获取测试用例表中的idx +2行
                caseRow =excelObj.getRow(caseSheet,idx +2)
                #获取第idx+2行,步骤sheet单元格内容
                caseStepSheetName = caseRow[testCase_testCaseName -1].value
                print caseStepSheetName

                #根据用例步骤名获取步骤sheet对象
                stepSheet = excelObj.getSheetByName(caseStepSheetName)
                #获取步骤sheet中步骤数
                stepNum=excelObj.getRowsNumber(stepSheet)
                print stepNum
                #记录测试用例中i步骤成功数
                successfulSteps = 0
                print u"开始执行用例 %s" %caseRow[testCase_testCaseName -1].value
                for step in xrange(2,stepNum+1):
                    #因为步骤sheet中的第一行为标题行，不需要执行
                    #获取步骤sheet中第step行对象
                    stepRow = excelObj.getRow(stepSheet,step)
                    #获取关键字作为调用的函数名
                    keyWord = stepRow[testStep_keyWords -1].value
                    #获取操作元素定位方式作为调用的函数参数
                    locationType = stepRow[testStep_locationType -1].value
                    # 获取操作元素定位表达式作为调用的函数参数
                    locationExpression = stepRow[testStep_locationExpression -1].value
                    #获取操作值作为调用函数的参数
                    operateValue = stepRow[testStep_operateValue -1].value

                    #将操作值为数字类型的数据转换成字符串类型，方面字符串拼接
                    if isinstance(operateValue,long):
                        operateValue = str(operateValue)
                    print  keyWord,locationExpression,operateValue

                    expressionStr = ""

                    #构造需要执行的Python语句
                    #对应的是PageAction.py文件中的页面动作函数调用的字符串表示

                    if  keyWord and operateValue and locationType is None and locationExpression is None:
                        expressionStr = keyWord.strip() +  "(u'" + operateValue+"')"
                    elif keyWord and operateValue is None and locationType is None and locationExpression is None:
                        expressionStr = keyWord.strip() + "()"
                    elif keyWord and locationType and operateValue and locationExpression is None:
                        expressionStr = keyWord.strip() + "('" + locationType.strip()+"',u'" + operateValue+"')"
                    elif keyWord and locationType and locationExpression and operateValue:
                        expressionStr = keyWord.strip() + "('" + locationType.strip() +"','"+ locationExpression.replace(",",'"').strip()+"',u'"+operateValue+"')"
                    elif keyWord and excelObj and locationExpression and operateValue is None:
                        expressionStr = keyWord.strip()+ "('"+ locationType.strip()+"','"+locationExpression.replace(",",'"').strip()+"')"
                    print expressionStr

                    try:
                        #通过eval函数，将拼接的页面动作函数调用的自渡船表示
                        #当成有效的Python表达式执行，从而执行测试步骤的sheet
                        #关键字在action.py文件中对应的映射方法
                        #来完成对页面元素的操作
                        eval(expressionStr)
                        #在测试执行时间列写入执行时间
                        excelObj.writeCellCurrentTime(stepSheet,rowNo=step,colsNo=testStep_runTime)
                    except Exception,e:
                        #截取异常屏幕图片
                        capturePic = capture_screen()
                        #获取详细的异常堆栈信息
                        errorInfo = traceback.format_exc()
                        #在测试步骤中sheet中写入失败信息
                        writeTestResult(stepSheet,step,"caseStep","failed",errorInfo,capturePic)
                        print u'步骤 "%s" 执行失败'  %stepRow[testStep_testStepDescribe -1].value
                    else:
                        #在测试步骤中sheet中写入成功信息
                        writeTestResult(stepSheet,step,"caseStep","pass")
                        #每成功一步，successfulsteps变量自增1
                        successfulSteps +=1
                        print u'步骤 "%s" 通过' %stepRow[testStep_testStepDescribe -1].value

                    if successfulSteps == successfulSteps -1:
                        #当测试用例步骤sheet中所有的步骤都执行成功
                        #方认为次测试用例执行通过，然后将成功信息写入测试用例工作表中，否则写入失败信息中去
                        writeTestResult(caseSheet,idx +2,"testCase","pass")
                        successfulCase +=1

                    else:
                        writeTestResult(caseSheet,idx +2,"testCase","failed")
                print u"共%d条用例，%d条需要被执行，本次执行通过%d条" %(len(isExecuteColumn)-1,requireCase,successfulCase)
    except Exception,e:
        #打印详细的异常堆栈信息
        print traceback.print_exc()

if __name__ == '__main__':
    TestSendMailWithAttachment()



































""" 
####调用页面动作执行自动化发送邮件###
def TestSendMailWithAttachment():
    from selenium import webdriver
    print u"启动Firefox浏览器"
    open_browser('firefox')
    maximize_browser()
    print u"访问126邮箱登录页"
    visit_url("http://mail.126.com")
    sleep(5)
    assert_string_in_pagesource(u"126网易免费邮--你的专业电子邮局")
    print u"访问126邮箱登录页成功"
    #driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    #waitFrameToBeAviailableAndSwitchToIt("id","x-URS-iframe")
    waitFrameToBeAviailableAndSwitchToIt("id", '//iframe[contains(@id,"iframe")]')
    #wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[contains(@id,"x-URS-iframe")]')))

    print u"输入登录的用户名"
    input_string("xpath",'//input[@name="email"]',"wangyh_0516ok")
    print u"输入登录密码"
    input_string("xpath", "//input[@name='password']","1502070803")
    click("id","dologin")
    sleep(5)
    assert_title(u"网易邮箱")
    print "登录成功"

    waitVisibilityOfElementLocated("xpath","//span[text()='写 信']")
    click("xpath","//span[text()='写 信']")
    print u"开始写信"
    print u"输入邮件地址"
    input_string("xpath","//div[contains(@id,'_mail_emailinput')]/input","844649600@qq.com")
    print u"输入邮件主题"
    input_string("xpath","//div[@aria-label='邮件主题输入框，请输入邮件主题']/input",u"0207新邮件01")
    print u"单击上传按钮附件"
    click("xpath","//div[contains(@title,'点击添加附件')]")
    sleep(3)
    print u"上传附件"
    paste_string(u"/Users/wangyanhua/Desktop/text181215.txt")
    press_enter_key()
    waitFrameToBeAviailableAndSwitchToIt("xpath","//iframe[@tabindex=1]")
    print u"写入邮件正文"
    input_string("xpath","/html/body",u"0207邮件正文01")
    switch_to_default_content()
    print u"写信完成"
    print u"开始发送邮件"
    click("xpath","//header//span[text()='发送']")
    time.sleep(3)
    assert_string_in_pagesource(u"发送成功")
    print u"邮件发送成功"
    close_browser()

if __name__ == '__main__':
    TestSendMailWithAttachment()

"""


""" 
####简单的测试逻辑代码#####
def TestSendMailWithAttachment():
    #创建Chrome浏览器的实例
    driver = webdriver.Firefox(executable_path="/Users/wangyanhua/Documents/学习/Python/webdrive/geckodriver")  # 调取火狐浏览器
    #driver = webdriver.Chrome(executable_path="/Users/wangyanhua/Documents/学习/Python/webdrive/chromedriver")
    #最大化浏览器窗口
    driver.maximize_window()
    print u"浏览器启动成功"
    print u"访问126邮箱登录页"
    driver.get("http://mail.126.com")
    #暂停5秒，以便登录邮箱加载完成
    time.sleep(5)
    assert u"126网易免费邮--你的专业电子邮局" in driver.title
    print u"访问126邮箱登录页成功"

    wait = WaitUtil(driver)
    #wait.frame_available_and_switch_to_it("id","x-URS-iframe")
    # wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID,"x-URS-iframe")))
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))


    print u"输入登录的用户名"
    username = getElement(driver,"xpath",'//input[@name="email"]')
    username.send_keys("wangyh_0516ok")
    print u"输入登录密码"
    password = getElement(driver,"xpath","//input[@name='password']")
    password.send_keys("1502070803")
    print u"登录..."
    password.send_keys(Keys.RETURN)

    #等待5秒，以便登录成功好后的页面加载完成
    time.sleep(5)
    assert u"网易邮箱" in driver.title
    print "登录成功"

    driver.switch_to.default_content()  # 添加的代码
    element = wait.visibility_element_located("xpath","//span[text()='写 信']")
    element.click()
    print u"写信..."
    #receiver = getElement(driver,"xpath","//div[contains(@id,'_mail_emailinput')]/input")
    driver.find_element_by_xpath("//div[contains(@id,'_mail_emailinput')]/input").send_keys("844649600@qq.com")
    #输入收信人地址
    #receiver.send_keys("844649600@qq.com")
    subject = getElement(driver,"xpath","//div[@aria-label='邮件主题输入框，请输入邮件主题']/input")
    subject.send_keys(u"0205新邮件01")

    #设置剪贴板内容
    Clipboard.setClipboardData(u"/Users/wangyanhua/Desktop/text181215.txt")
    #获取剪贴板内容
    Clipboard.getClipboardData()
    attachment = getElement(driver,"xpath","//div[contains(@title,'点击添加附件')]")
    #attachment = getElement(driver, "xpath", "//div[contains(@title,'600首MP3')]")
    #单击上传附件
    attachment.click()
    time.sleep(3)


    #上传时，黏贴剪贴内容????
    ActionChains(driver).key_down(Keys.COMMAND).send_keys("v").key_up(Keys.COMMAND).perform()
    #模拟回车键盘???
    ActionChains(driver).send_keys(Keys.ENTER)


    wait.frame_available_and_switch_to_it("xpath","//iframe[@tabindex=1]")
    body = getElement(driver,"xpath","/html/body")
    #输入邮件正文
    body.send_keys(u"发送光荣之路的测试邮件正文020602")
    #切出邮件正文的frame框
    driver.switch_to.default_content()

    print u"写信完成"
    getElement(driver,"xpath","//header//span[text()='发送']").click()
    print u"开始发送邮件"
    time.sleep(3)
    assert u"发送成功" in driver.page_source
    print u"邮件发送成功"
    driver.quit()

if __name__ == '__main__':
    TestSendMailWithAttachment()

"""






