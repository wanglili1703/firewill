# coding=utf-8
import os

from appium import webdriver as app_driver

from _common.utility import Utility


class WebDriver:
    class Appium():
        def __init__(self):
            self.web_driver = None

        def open_android_app(self, app_path, platform_version, device_id, port, package_name, full_reset='false'):
            self.desired_caps = {}
            self.desired_caps['platformName'] = 'Android'
            self.desired_caps['platformVersion'] = platform_version
            self.desired_caps['deviceName'] = 'Android'
            self.desired_caps['app'] = app_path
            self.desired_caps['udid'] = device_id
            self.desired_caps['fullReset'] = full_reset
            self.desired_caps['appActivity'] = 'com.shhxzq.xjb.ui.LoadingActivity'
            self.desired_caps['appPackage'] = package_name
            self.desired_caps['unicodeKeyboard'] = 'true'
            self.desired_caps['resetKeyboard'] = 'true'

            self.web_driver = app_driver.Remote('http://localhost:%s/wd/hub' % port, self.desired_caps)
            return self.web_driver

        def open_ios_app(self, app_path, platform_version, device_id, port, package_name, full_reset='false'):
            self.desired_caps = {}
            self.desired_caps['platformName'] = 'iOS'
            self.desired_caps['platformVersion'] = platform_version
            self.desired_caps['deviceName'] = 'iOS'
            self.desired_caps['noReset'] = 'true'
            self.desired_caps['app'] = app_path
            self.desired_caps['bundleId'] = package_name
            self.desired_caps['udid'] = device_id
            self.desired_caps['fullReset'] = full_reset
            self.desired_caps['appActivity'] = 'com.shhxzq.xjb.ui.LoadingActivity'
            self.desired_caps['appPackage'] = 'com.shhxzq.xjbEnt'
            self.desired_caps['unicodeKeyboard'] = 'true'
            self.desired_caps['resetKeyboard'] = 'true'

            print 'open ios app'
            try:
                self.web_driver = app_driver.Remote('http://localhost:%s/wd/hub' % port, self.desired_caps)
            except Exception, e:
                print 'open ios failure'
                print e
                # ids = os.popen("ps -ef|grep 'iOS'|grep 'appium'|awk '{print $2}'", 'r').readlines()
                # print 'start to kill ios appium'
                # if len(ids) >= 2:
                #     os.system('kill -9 %s' % ids[1])
                # print 'restart appium'
                # os.system(
                #     'appium --address 127.0.0.1 --port 4723 --session-override --platform-name "iOS" --platform-version 1.6.5 &')
                #
                # print 'reinitiate web driver'
                # self.web_driver = app_driver.Remote('http://localhost:%s/wd/hub' % port, self.desired_caps)
            return self.web_driver
