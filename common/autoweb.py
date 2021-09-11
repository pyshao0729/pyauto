from selenium import webdriver
import time,os
from comm import logger
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
class AutoWeb():
    def __init__(self):
        """[初始化web对象，并将窗口最大化]
        """        
        #self.driver = driver
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
    def open_url(self,url):
        """[打开url地址]

        Args:
            url ([str]): [网页地址url]
        """        
        self.driver.get(url)
        self.driver.implicitly_wait(30)
    #显性等待时间
    def wait_until_element_presence(self,timeout,id):
        locator = (By.ID, id)
        WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located(locator))
    def wait_until_text_presence(self,timeout,id,text):
        locator = (By.ID, id)
        WebDriverWait(self.driver,timeout).until(EC.text_to_be_present_in_element(locator,text))
    # selenium 定位方法
    def locate_element(self,locatetype,value):
        """[summary]

        Args:
            locatetype ([str]): [定位标签类型，取值范围：id，name,class_name,tag_name,link,css,partial_link,xpath]
            value ([str]): [标签值]

        Returns:
            [obj]: [返回定位的元素对象]
        """        
        if (locatetype == 'id'):
            el = self.driver.find_element_by_id(value)
        if (locatetype == 'name'):
            el = self.driver.find_element_by_name(value)
        if (locatetype == 'class_name'):
            el = self.driver.find_element_by_class_name(value)
        if (locatetype == 'tag_name'):
            el = self.driver.find_elements_by_tag_name(value)
        if (locatetype == 'link'):
            el = self.driver.find_element_by_link_text(value)
        if (locatetype == 'css'):
            el = self.driver.find_element_by_css_selector(value)
        if (locatetype == 'partial_link'):
            el = self.driver.find_element_by_partial_link_text(value)
        if (locatetype == 'xpath'):
            el = self.driver.find_element_by_xpath(value)
        return el if el else None

    #切换frame
    def switch_to_frame(self,framename):
        """[切换web框架]

        Args:
            framename ([str]): [框架name值]
        """        
        self.driver.switch_to.frame(framename)
    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
    #切换到弹出窗口
    def switch_to_alert(self):
        self.driver.switch_to.alert.accept()
    #刷新当前页面
    def refresh(self):
        self.driver.refresh()
    #窗口截图
    def get_screenshot_as_file(self,filename):
        """[窗口截图]

        Args:
            filename ([str]): [截图文件名]
        """        
        self.driver.get_screenshot_as_file(filename)

    #鼠标点击
    def mouse_click(self,locatetype=None,value=None):
        """[鼠标点击]

        Args:
            locatetype ([str], optional): [定位标签类型，取值范围：id，name,class_name,tag_name,link,css,partial_link,xpath,或不传此参数]. Defaults to None.
            value ([str], optional): [标签值，若不传locatetype，则此参数也不传]. Defaults to None.
        """        
        onElement=self.locate_element(locatetype, value) if value is not None else None
        ActionChains(self.driver).click(onElement)
    #鼠标双击
    def mouse_doubleclick(self,locatetype=None,value=None):
        """[鼠标双击]

        Args:
            locatetype ([str], optional): [定位标签类型，取值范围：id，name,class_name,tag_name,link,css,partial_link,xpath,或不传此参数]. Defaults to None.
            value ([str], optional): [标签值，若不传locatetype，则此参数也不传]. Defaults to None.
        """        
        onElement=self.locate_element(locatetype, value) if value is not None else None
        ActionChains(self.driver).double_click(onElement)

    #鼠标移动至某个元素
    def mouse_move_to_element(self,locatetype, value):
        """[鼠标移动至某个元素]

        Args:
            locatetype ([str]): [定位标签类型，取值范围：id，name,class_name,tag_name,link,css,partial_link,xpath]
            value ([str]): [标签值]
        """        
        moveToElement = ActionChains(self.driver).move_to_element(self.locate_element(locatetype, value))
        moveToElement.perform()
    #鼠标移动至距当前位置x,y处
    def mouse_move_by_offset(self,offsetx,offsety):
        """[鼠标移动至距当前位置x,y处]

        Args:
            offsetx ([float]): [偏移的水平像素，可为负数]
            offsety ([float]): [偏移的垂直像素，可为负数]
        """        
        ActionChains(self.driver).move_by_offset(offsetx,offsety).perform()
    #鼠标移动至距离某个元素x,y距离处
    def mouse_move_to_element_with_offset(self,toElement, offsetx,offsety):
        """[鼠标移动至距离某个元素x,y距离处]

        Args:
            toElement ([str]): [起始定位元素，可以用locate_element方法获取]
            offsetx ([float]): [偏移的水平像素，可为负数]
            offsety ([float]): [偏移的垂直像素，可为负数]
        """        
        ActionChains(self.driver).move_to_element_with_offset(toElement,offsetx,offsety).perform()
    #鼠标在定位元素按下，并且偏移x,y
    def mouse_clickhold_move_to_element_with_offset(self,locateElement,offsetx,offsety):
        """[鼠标在定位元素按下，并且偏移x,y]

        Args:
            locateElement ([str]): [起始定位元素，可以用locate_element方法获取]
            offsetx ([float]): [偏移的水平像素，可为负数]
            offsety ([float]): [偏移的垂直像素，可为负数]
        """        
        ActionChains(self.driver).move_to_element_with_offset(locateElement,offsetx,offsety).click_and_hold().perform()
    #鼠标在定位元素拖拽并偏移x,y
    def mouse_drag_and_drop_to(self,dragElement,offsetx,offsety):
        """[鼠标在定位元素拖拽并偏移x,y]

        Args:
            dragElement ([str]): [拖拽起始位置元素，可以用locate_element方法获取]
            offsetx ([float]): [偏移的水平像素，可为负数]
            offsety ([float]): [偏移的垂直像素，可为负数]
        """        
        ActionChains(self.driver).drag_and_drop_by_offset(dragElement,offsetx,offsety).perform()
    #鼠标在定位元素左键按下
    def mouse_click_hold(self,locatetype=None, value=None):
        """[按下鼠标左键]

        Args:
            locatetype ([str], optional): [定位标签类型，取值范围：id，name,class_name,tag_name,link,css,partial_link,xpath,或不传此参数]. Defaults to None.
            value ([str], optional): [标签值，若不传locatetype，则此参数也不传]. Defaults to None.
        """        
        if locatetype==None:
            clickHold = ActionChains(self.driver).click_and_hold()
        else:
            clickHold = ActionChains(self.driver).click_and_hold(self.locate_element(locatetype, value))
        clickHold.perform()
    #释放鼠标左键
    def mouse_release(self,locatetype=None,value=None):
        """[释放鼠标左键]

        Args:
            locatetype ([str], optional): [定位标签类型，取值范围：id，name,class_name,tag_name,link,css,partial_link,xpath,或不传此参数]. Defaults to None.
            value ([str], optional): [标签值，若不传locatetype，则此参数也不传]. Defaults to None.
        """        
        moseRelease = ActionChains(self.driver).release(self.locate_element(locatetype, value))
        moseRelease.perform()

    # selenium 点击
    def click(self,locatetype,value):
        """[在指定元素上点击]

        Args:
            locatetype ([str]): [定位标签类型，取值范围：id，name,class_name,tag_name,link,css,partial_link,xpath]
            value ([str]): [标签值]
        """        
        self.locate_element(locatetype,value).click()
 
    #selenium 输入
    def input_data(self,locatetype,value,data):
        """[指定input框内输入数据]

        Args:
            locatetype ([str]): [定位标签类型，取值范围：id，name,class_name,tag_name,link,css,partial_link,xpath]
            value ([str]): [标签值]
            data ([str]): [要输入的数据]]
        """        
        self.locate_element(locatetype,value).clear()
        self.locate_element(locatetype,value).send_keys(data)
    #获取定位到的指定元素
    def get_text(self, locatetype, value):
        """[获取指定标签的文本]

        Args:
            locatetype ([str]): [定位标签类型，取值范围：id，name,class_name,tag_name,link,css,partial_link,xpath]
            value ([str]): [标签值]

        Returns:
            [str]: [指定标签的文本]
        """        
        return self.locate_element(locatetype, value).text
    # 获取标签属性
    def get_attr(self, locatetype, value, attr):
        """[获取标签属性]

        Args:
            locatetype ([str]): [定位标签类型，取值范围：id，name,class_name,tag_name,link,css,partial_link,xpath]
            value ([str]): [标签值]
            attr ([str]): [标签属性]

        Returns:
            [str]: [标签属性]
        """        
        return self.locate_element(locatetype, value).get_attribute(attr)

    #通过select索引选择下拉框
    def select_by_index(self,locatetype,value,index):
        """[通过select索引选择下拉框]

        Args:
            locatetype ([str]): [定位标签类型，取值范围：id，name,class_name,tag_name,link,css,partial_link,xpath]
            value ([str]): [标签值]
            index ([int]): [下拉菜单索引值，从0计数]
        """        
        Select(self.locate_element(locatetype, value)).select_by_index(index)
    #通过select的value选择下拉框
    def select_by_value(self,locatetype,value,svalue):
        """[通过select的value选择下拉框]

        Args:
            locatetype ([str]): [定位标签类型，取值范围：id，name,class_name,tag_name,link,css,partial_link,xpath]
            value ([str]): [标签值]
            svalue ([str]): [下拉菜单value值]
        """        
        Select(self.locate_element(locatetype, value)).select_by_value(svalue)
    #获取第一个选项
    def first_selected_option(self,locatetype,value):
        return Select(self.locate_element(locatetype, value)).first_selected_option.text
    #获取下拉菜单所有选项
    def all_select_options(self,locatetype,value):
        return Select(self.locate_element(locatetype, value)).options
        

    #web登陆
    def login_web(self,username,password,webtype="v7"):
        """[web登陆]

        Args:
            username ([str]): [web登陆用户名]
            password ([str]): [web登陆密码]
            webtype (str, optional): [产品web类型，取值范围:v7,edgeos，默认v7]. Defaults to "v7".

        Returns:
            [bool]: [False,True]
        """        
        logger.info("开始登陆：")
        time.sleep(1)
        self.input_data("id","username",username)
        time.sleep(1)
        self.input_data("id","password",password)
        time.sleep(1)
        if webtype is "v7":
            logbutton = "butLogin"
        elif webtype is "edgeos":
            logbutton = "button"
        else:
            raise("未定义的web类型:%s！"%webtype)
        self.click("id",logbutton)
        #self.driver.find_element_by_id('butLogin').click()
        time.sleep(5)
        u=self.driver.current_url
        if "main.htm" in u:
            logger.info("登陆成功！")
            return True
        else:
            logger.error("登陆失败！")
            return False
    #web关闭
    def logout_web(self):
        """[web关闭]
        """        
        self.driver.quit()

    #pt控制
    def pt_control(self,weblocation,derection,movetime=5):
        """[云台控制]

        Args:
            weblocation ([string]): [web页面所在位置，取值范围：main，inner]
            derection ([string]): [云台转动方向，取值范围：left，right，up，down，leftup，leftdown，rightup，rightdown]
            movetime (int, optional): [鼠标按下时间，默认为5秒]. Defaults to 5.

        Returns:
            [bool]: [True,False]
        """        
        innerPT = {
            "left":"left",
            "right":"right",
            "up":"up",
            "down":"down",
            "leftup":"leftup",
            "leftdown":"leftdown",
            "rightup":"rightup",
            "rightdown":"rightdown",
        }
        mainPT = {
            "left":"ptz_left",
            "right":"ptz_right",
            "up":"ptz_up",
            "down":"ptz_down",
            "leftup":"ptz_leftup",
            "leftdown":"ptz_leftdown",
            "rightup":"ptz_rightup",
            "rightdown":"ptz_rightdown",
        }

        if weblocation=="main":
            
            logger.info("点击云台向{0}，等待结束。。。".format(derection))
            self.mouse_move_to_element("id",mainPT[derection])
            self.mouse_click_hold("id",mainPT[derection])
            time.sleep(movetime)
            self.mouse_release()
        elif weblocation=="inner":

            logger.info("点击云台向{0}，等待结束。。。".format(derection))
            self.mouse_move_to_element("id",innerPT[derection])
            self.mouse_click_hold("id",innerPT[derection])
            time.sleep(movetime)
            self.mouse_release()
        else:
            logger.error("未定义的web位置：{0}，weblocation只能为main或inner".format(weblocation))
            return False
    #zoom控制
    def zoom_control(self,weblocation,zoom,movetime=5):
        """[变倍控制]

        Args:
            weblocation ([str]): [web页面所在位置，取值范围：main，inner]
            zoom ([str]): [变倍类型，取值范围：zoomin，zoomout]
            movetime (int, optional): [鼠标按下时间，默认为5秒]. Defaults to 5.

        Returns:
            [bool]: [True,False]
        """        
        innerZoom = {
            "zoomin":"zoomIn",
            "zoomout":"zoomOut",
        }
        mainZoom = {
            "zoomin":"ptz_zoomIn",
            "zoomout":"ptz_zoomOut",
        }
        if weblocation=="main":
            logger.info("点击{0}，等待结束。。。".format(zoom))
            self.mouse_move_to_element("id",mainZoom[zoom])
            self.mouse_click_hold("id",mainZoom[zoom])
            time.sleep(movetime)
            self.mouse_release()
        elif weblocation=="inner":
            logger.info("点击{0}，等待结束。。。".format(zoom))
            self.mouse_move_to_element("id",innerZoom[zoom])
            self.mouse_click_hold("id",innerZoom[zoom])
            time.sleep(movetime)
            self.mouse_release()
        else:
            logger.error("未定义的web位置：{0}，weblocation只能为main或inner".format(weblocation))
            return False
    #focus控制
    def focus_control(self,weblocation,focus,movetime=5):
        """[聚焦]

        Args:
            weblocation ([str]): [web页面所在位置，取值范围：main，inner]
            focus ([str]): [聚焦控制类型，取值范围：focusin，focusout，focusauto]
            movetime (int, optional): [鼠标按下时间，默认为5秒]. Defaults to 5.

        Returns:
            [bool]: [True,False]
        """        
        innerFocus = {
            "focusin":"PushIn",
            "focusout":"PullAway",
            "focusauto":"focusautoPush",
        }
        mainFocus = {
            "focusin":"ptz_PushIn",
            "focusout":"ptz_PullAway",
            "focusauto":"ptz_focusautoPush",
        }
        if weblocation=="main":
            logger.info("点击{0}，等待结束。。。".format(focus))
            self.mouse_move_to_element("id",mainFocus[focus])
            self.mouse_click_hold("id",mainFocus[focus])
            time.sleep(movetime)
            self.mouse_release()
        elif weblocation=="inner":
            logger.info("点击{0}，等待结束。。。".format(focus))
            self.mouse_move_to_element("id",innerFocus[focus])
            self.mouse_click_hold("id",innerFocus[focus])
            time.sleep(movetime)
            self.mouse_release()
        else:
            logger.error("未定义的web位置：{0}，weblocation只能为main或inner".format(weblocation))
            return False


    

''' 
webdrv = AutoWeb()
webdrv.open_url("http://10.67.38.119")
webdrv.login_web("admin","admin123","v5")

time.sleep(5)

webdrv.logout_web()
'''