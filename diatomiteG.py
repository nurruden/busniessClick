# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: diatomiteG
@time: 2023/10/27 13:50
"""
# coding=utf-8
from selenium import webdriver
import requests,time,re
import fake_useragent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
import logging
from logging.config import fileConfig

fileConfig("./busniessClick/conf/logging_config.ini")
logger = logging.getLogger()
logger.debug('often makes a very good meal of %s', 'visiting tourists')


class Viewer:
    driver_path = "./busniessClick/drivers/chromedriver"  #定义浏览器驱动的位置
    final_url = None

    def __init__(self,kw,title):
        self.bdurl = "https://www.baidu.com/s?wd="
        self.bdurl_base = "https://www.baidu.com/"
        self.kw = kw
        self.title = title
        self.ua=fake_useragent.UserAgent()

    #将request请求返回的cookie转为字符串或者字典形式,默认转为字符串形式
    def handleRequestCookie(self,cookies,type=0):
        cookies_dict =  cookies.get_dict()
        if type==0:
            result = ""
            for index in cookies_dict:
                result = result+"%s=%s; " % (index,cookies_dict[index])
        else:
            result = cookies_dict
        logger.info("The cookie is: %s",result)

        return result


    #先访问百度首页,获取其cookie,再用这个cookie去访问搜索页,这是为了防百度的验证,如果搜索多了就会出现这个验证
    def getBaiduCookie(self):
        headers = {"User-Agent":self.ua.random}
        r = requests.get(self.bdurl_base,headers=headers)
        self.bdCookies = r.cookies

    #初始化浏览器
    def init_chrome(self):
        opt = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}  # 无图模式
        opt.add_experimental_option("prefs",prefs)
        opt.add_argument("user-agent="+self.ua.random)   #添加随机user-agent
        logger.info("The random agent is: %s",self.ua.random)
        driver = webdriver.Chrome(executable_path=self.driver_path,options=opt)

        self.driver = driver

    # 处理每页获取到的百度搜索,并处理掉里面的html,匹配self.title
    def matchTitle(self,items):
        self.lastItems = items
        for i,item in zip(range(len(items)),items):
            # print(20*"*"+"i,item"+20*"*")
            # print(str(i)+'\n')
            # print(item)
            # print(item)
            # 获取每个节点的html,去除里面的标签
            html = item.get_attribute("innerHTML")
            # print(40 * "-" + "html" + 40 * "-")
            # print(html)
            html = re.sub("</?[^<>]+>","",html)
            # print(60 * "^" + "bref html" + 60 * "^")
            # print(html)
            #
            # print("*"*90)

            # print(html.title())
            if html.find(self.title)!=-1:
                return i

        return False


    # 搜索关键词
    def search(self):
        self.driver.implicitly_wait(10)   # 设置10秒的隐性等待时间
        self.driver.get(self.bdurl_base)
        print(self.kw)
        self.driver.find_element(By.ID,'kw').send_keys(self.kw)
        self.driver.find_element(By.ID,'su').click()

        # 获取每一页的每一条的内容,如果在这一条内容上找到self.title的内容,就获取他的下标
        # items = self.driver.find_elements(By.XPATH,"//h3[contains(@class,'t ec_title')]/a")
        items = self.driver.find_elements(By.CSS_SELECTOR,".EC_result")
        # print(self.title)
        # print(items)
        #
        # print(len(items))
        # for i  in items:
        #     print(i)
        click_index = self.matchTitle(items)

        if click_index is False:
            #如果没有找到self.title的内容,就点击下一页重复上面的过程
            while click_index is False:  # is相当于python中的全等于
                #点击下方分页的下一页,如果没有则跳出
                try:
                    self.driver.find_element(By.XPATH,"//div[@id='page']/strong/following-sibling::*[1]").click()
                    # time.sleep(2)
                    WebDriverWait(self.driver, 10, 0.5).until(lambda driver:self.driver.find_elements(By.CSS_SELECTOR,".EC_result") and self.lastItems!=self.driver.find_elements(By.CSS_SELECTOR,".EC_result"))
                    items = self.driver.find_elements(By.CSS_SELECTOR,".EC_result")
                    click_index = self.matchTitle(items)
                    # print(click_index)

                    if click_index is not False:
                        print(40*"@"+"items index"+40*"@")
                        # print(items[click_index])
                        items[click_index].click()    #找到则点击链接,并停留1分钟
                        time.sleep(60)
                        self.final_url = self.driver.current_url
                        # self.driver.quit()

                        self.res=True    # 最终结果,直接在类外部用对象.res查看最终结果
                except BaseException as e:
                    self.res=False
                    break
        else:
            self.final_url = self.driver.current_url
            # print(self.final_url)
            # print(items[click_index])

            # agent = self.driver.execute_script("return navigator.userAgent")
            # print(agent)
            items[click_index].click()
            sleep(30)
            # print(self.driver.page_source)
            sleep(30)
            # print(self.driver.save_screenshot("/Users/northstar/pythontest/screenshot/1.png"))

            self.res = True  # 最终结果,直接在类外部用对象.res查看最终结果

        self.driver.quit()
        #关闭浏览器



    # 执行搜索,并翻页,找到self.title之后直接点击进去

    def run(self):
        # 初始化浏览器
        self.init_chrome()

        # 请求百度首页,并且输入title,点击搜索
        self.search()

if __name__=="__main__":
    # 搜索php教程这个关键词，要点击指定的title的链接，如果这个title在百度没有排名则点击不到
    # viewer = Viewer(kw="硅藻土",title="嵊州市华力硅藻土制品有限公司-硅藻土_硅藻土助滤剂_硅藻土生产厂家")
    # viewer = Viewer(kw="硅藻土", title="森大")
    # viewer = Viewer(kw="硅藻土", title="环阳矿产")
    viewer = Viewer(kw="硅藻土", title="阿拉丁")
    viewer.run()
    # sleep(60)
    # print(viewer.res)
    # print(viewer.final_url)
