# coding=utf8
# Created on July 19, 2018
# @author: luning644182206@emails.bjut.edu.cn

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Firefox
# from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

# 定义一个类作为驱动
class DriverCommon:
    options = ''
    driver = ''
    wait = ''
    def __init__(self):
        self.options = Options()
        self.options.add_argument('-headless')  # 无头参数
        self.driver = Firefox(executable_path='./third_party/geckodriver', firefox_options = self.options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
        # self.driver = Chrome(executable_path='./third_party/geckodriver', chrome_options = self.options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
        self.wait = WebDriverWait(self.driver, timeout = 15) # 设置成15