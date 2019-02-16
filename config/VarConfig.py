#encoding=utf-8
import os
firefoxDriverFilePath= "/Users/wangyanhua/Documents/学习/Python/webdrive/geckodriver"
chromeDriverFilePath= "/Users/wangyanhua/Documents/学习/Python/webdrive/chromedriver"
ieDriverFilePath = "/Users/wangyanhua/Documents/学习/Python/webdrive/IEDriverServer"

#当前文件所在目录的父目录的绝对路径
parentDirPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print parentDirPath
#异常截图存放目录绝对路径
screenPicturesDir = parentDirPath + "/exceptionpictures/"
#print screenPicturesDir

#测试数据文件存放的绝对路径
dataFilePath = parentDirPath + '/testData/126邮箱发送邮件.xlsx'
#print dataFilePath


#测试数据文件中，测试用例对应的数字序号
testCase_testCaseName= 2
testCase_testStepSheetName= 4
testCase_isExecute= 5
testCase_runTime = 6
testCase_testResult = 7

#用例步骤中，部分对应的数字序号
testStep_testStepDescribe = 2
testStep_keyWords = 3
testStep_locationType = 4
testStep_locationExpression = 5
testStep_operateValue = 6
testStep_runTime =7
testStep_testResult = 8
testStep_errorInfo =9
testStep_errorPic = 10











