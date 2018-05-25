# coding = utf-8
import sys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
from io import BytesIO
from PIL import Image

BORDER = 6
INIT_LEFT = 60
webDriverPath = "D:\software\chromedriver.exe" # chromedriver.exe存放位置
webUrl = 'https://passport.cnblogs.com/user/signin?ReturnUrl=https%3A%2F%2Fwww.cnblogs.com%2F'

USERNAME = 'x' # 博客园用户名
PASSWORD = 'x' # 博客园密码

class CrackCnblog():
    def __init__(self):
        self.url = webUrl
        self.browser = webdriver.Chrome(executable_path=webDriverPath)
        self.wait = WebDriverWait(self.browser, 10)
        self.username = USERNAME
        self.password = PASSWORD

    # when destory class
    def __del__(self):
        self.browser.close()

    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)

    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def open(self):
        browser = self.browser
        browser.get(webUrl)
        input1 = browser.find_element_by_id('input1')  # username  geetest_wait
        input2 = browser.find_element_by_id('input2')  # pwd
        signin = browser.find_element_by_id('signin')

        input1.send_keys('maduar')
        input2.send_keys('A@maduar310')
        signin.click()

        # wait cpa  browser.find_element_by_class_name('geetest_canvas_fullbg')
        wait = WebDriverWait(browser, 20)
        geetSliderButton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        geetSliderButton.click()
        # geetest_canvas_fullbg geetest_fade geetest_absolute

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()
    def login(self):
        """
        登录
        :return: None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
        submit.click()
        time.sleep(10)
        print('登录成功')

    def crackImg(self):
        image1 = self.get_geetest_image('captcha1.png')
        # 点按呼出缺口
        geetButton = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        geetButton.click()

        # 获取带缺口的验证码图片
        image2 = self.get_geetest_image('captcha2.png')
        # 获取缺口位置
        gap = self.get_gap(image1, image2)
        print('缺口位置', gap)

        # 减去缺口位移
        gap -= BORDER
        # 获取移动轨迹
        track = self.get_track(gap)
        print('滑动轨迹', track)
        # 拖动滑块
        self.move_to_gap(geetButton, track)

    def again_login(self):
        self.crackImg()
        self.veritySuccess()


    def veritySuccess(self):
        success = None
        try:
            # x修改等待时间
            wait = WebDriverWait(self.browser, 5)
            success = wait.until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功')
            )
        except TimeoutException as err:
            # 点按呼出缺口
            try:
                geetButton = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_reset_tip_content')))
                geetButton.click()
            except TimeoutException:
                self.browser.find_element_by_class_name("geetest_refresh_1").click()
        except Exception as err:
            self.browser.find_element_by_class_name("geetest_refresh_1").click()
            time.sleep(1)

        # 失败后重试
        if not success:
            print("login erro")
            self.again_login()
        else:
            # 如何判断页面跳转成功
            success_wait = WebDriverWait(self.browser, 2)
            page_success = success_wait.until(
                EC.element_to_be_clickable((By.ID, 'span_userinfo'))
            )
            if page_success:
                print("current_url: " + self.browser.current_url)
                print("current_url: " + json.dumps(self.browser.get_cookies()))
                print("login in")
            else:
                print("login fail")
                # 博客园 - 开发者的网上家园


    def crack(self):
        # 输入用户名密码
        self.open()
        self.crackImg()
        self.veritySuccess()

if __name__ == '__main__':
    crack = CrackCnblog()
    crack.crack()
