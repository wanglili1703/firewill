# coding=utf-8

import inspect
import os
import time as time_
from decimal import *
import subprocess


def get_resource_root_path():
    string_separator = 'huaxin'
    current_module_path = inspect.getmodule(get_resource_root_path).__file__
    init_path = re.split(string_separator, current_module_path)[0]
    resource_path = os.path.normpath(os.path.join(init_path, string_separator))
    return resource_path


import datetime
import time
import re

import sys
from robot.api import logger
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.wait import WebDriverWait

from _common.global_config import GlobalConfig

reload(sys)
sys.setdefaultencoding("utf-8")

WebDriverWait_TimeOut = GlobalConfig.PageTimeControl.WebDriverWait_TimeOut
SwipePage_Time = GlobalConfig.PageTimeControl.SwipePage_Time
Scroll_Time = GlobalConfig.PageTimeControl.Scroll_Time
SwipePage_TryTime = GlobalConfig.PageTimeControl.SwipePage_TryTime
SCREEN_SHOT = GlobalConfig.PathControl.SCREEN_SHOT


class PageObject_(object):
    def __init__(self, web_driver, device_id=None):
        self.web_driver = web_driver
        self.device_id = device_id

        self._tag_map_find_element_by = {
            'xpath_': 'find_element_by_xpath',
            'xpathIOS_': 'find_element_by_xpath',
            'id_': 'find_element_by_id',
            'accId_': 'find_element_by_accessibility_id',
            'accIds_': 'find_elements_by_accessibility_id',
            'predicate_': 'find_element_by_ios_predicate',
            'swipe_': None,
            'axis_': None,
            'assert_': None,
            'getV_': None,
        }

        self._tag_map_function = {
            'a': 'click',
            'select': 'select',
            'input': 'input',
            'textarea': 'textarea',
            'div': 'click',
            'span': 'click',
            'li': 'click',
            'drag': 'drag_drop',
            'button': 'click',
            'img': 'click',
            'ul': 'click',
            'label': 'input',
            'android.widget.ImageButton': 'click',
            'android.widget.ToggleButton': 'click',
            'android.widget.EditText': 'input',
            'android.widget.EditText_click': 'click',
            'android.widget.Button': 'click',
            'android.widget.TextView': 'click',
            'android.widget.RadioButton': 'click',
            'android.widget.ImageView': 'click',
            'android.widget.RelativeLayout': 'click',
            'android.widget.CheckedTextView': 'click',
            'android.widget.CheckBox': 'click',
            'android.view.View': 'click',
            'android.widget.Image': 'click',
            'swipe_': 'swipe',
            'axis_': 'axis_click',
            'assert_': 'assert_value',
            'getV_': 'get_value',
            '*': 'click',
            'XCUIElementTypeTextField': 'input',
            'XCUIElementTypeButton': 'click',
            'XCUIElementTypeSecureTextField': 'input',
            'XCUIElementTypeCell': 'click',
            'XCUIElementTypeStaticText': 'click',
            'XCUIElementTypeOther': 'click',
            'UIAButton': 'click',
            'UIATextField': 'input',
            'UIASecureTextField': 'input',
            'UIATableCell': 'click',
            'UIAStaticText': 'click',
            'UIATextView': 'input',
            'UIAImage': 'click',
            'UIAElement': 'click',
            'UIAKey': 'click',
            'UIACollectionCell': 'click',
            'UIASearchBar': 'input',
            'UIASearchBarCLICK': 'click',
            'UIASwitch': 'click',
            'UIALink': 'click',
        }

    def screen_shot_(self):
        file_name = str(str(time.time()).replace('.', ''))

        self.web_driver.get_screenshot_as_file(SCREEN_SHOT + '%s.jpg' % file_name)

        logger.info('<a href="%s.jpg"><img src="%s.jpg" width="%s"></a>'
                    % (file_name, file_name, '250'), html=True)

    def get_size(self):

        width = self.web_driver.get_window_size()['width']
        height = self.web_driver.get_window_size()['height']

        return width, height

    def element_exist_(self, element, find_element_by='find_element_by_xpath', timeout=WebDriverWait_TimeOut):
        starttime = datetime.datetime.now()
        wait = WebDriverWait(self.web_driver, timeout)

        try:
            wait.until(lambda x: getattr(x, find_element_by)(element))

            endtime = datetime.datetime.now()
            during_time = (endtime - starttime).seconds

            print '//--- finding element %s within %s seconds---//' % (element, during_time)

            return True
        except:
            print '//--- element %s not exist---//' % element
            return False

    def is_displayed(self, element, find_element_by='find_element_by_xpath', timeout=WebDriverWait_TimeOut):
        start_time = datetime.datetime.now()
        wait = WebDriverWait(self.web_driver, timeout)

        try:
            target = wait.until(lambda x: getattr(x, find_element_by)(element))

            end_time = datetime.datetime.now()
            during_time = (end_time - start_time).seconds

            visible = target.is_displayed()

            print '//--- finding element %s within %s seconds and visibility is %s---//' % (
                element, during_time, visible)

            return visible

        except:
            print '//--- element %s not exist---//' % element

            return False

    def get_elements_with_same_id_(self, id):
        time.sleep(2)
        starttime = datetime.datetime.now()

        try:
            eles = self.web_driver.find_elements_by_id(id_=id)
            endtime = datetime.datetime.now()
            during_time = (endtime - starttime).seconds

            print '//--- finding element %s within %s seconds---//' % (id, during_time)
            return eles
        except Exception, e:
            print '//--- elements %s not exist---//' % id
            print e

    def click_by_link_text_(self, text):
        starttime = datetime.datetime.now()

        try:
            eles = self.web_driver.find_elements_by_link_text(text=text)
            endtime = datetime.datetime.now()
            during_time = (endtime - starttime).seconds

            print '//--- finding element %s within %s seconds---//' % (id, during_time)
            return eles
        except Exception, e:
            print '//--- elements %s not exist---//' % id
            print e

    def get_value_(self, element, find_element_by='find_element_by_xpath', timeout=WebDriverWait_TimeOut):
        starttime = datetime.datetime.now()
        wait = WebDriverWait(self.web_driver, timeout)

        try:
            ele = wait.until(lambda x: getattr(x, find_element_by)(element))
            endtime = datetime.datetime.now()
            during_time = (endtime - starttime).seconds

            print '//--- finding element %s within %s seconds---//' % (element, during_time)
            return ele.text
        except Exception, e:
            print '//--- element %s not exist---//' % element
            print e

    def get_attribute_(self, element, attribute, find_element_by='find_element_by_xpath',
                       timeout=WebDriverWait_TimeOut):
        start_time = datetime.datetime.now()
        wait = WebDriverWait(self.web_driver, timeout)

        try:
            ele = wait.until(lambda x: getattr(x, find_element_by)(element))
            end_time = datetime.datetime.now()
            during_time = (end_time - start_time).seconds

            print '//--- finding element %s within %s seconds---//' % (element, during_time)
            return ele.get_attribute(attribute)
        except Exception, e:
            print '//--- element %s not exist---//' % element
            print e

    def is_overlapped_(self, element, find_element_by='find_element_by_xpath',
                       timeout=WebDriverWait_TimeOut):
        flag = False
        start_time = datetime.datetime.now()
        wait = WebDriverWait(self.web_driver, timeout)

        try:
            ele = wait.until(lambda x: getattr(x, find_element_by)(element))
            end_time = datetime.datetime.now()
            during_time = (end_time - start_time).seconds

            print '//--- finding element %s within %s seconds---//' % (element, during_time)

            width, heigth = self.get_size()
            # ele_x = ele.location['x']+ele.size['width']/2
            ele_y = ele.location['y'] + ele.size['height'] / 2
            ratio = ele_y / heigth

            if ratio > 0.92:  # 若被点击元素的中心位置的纵坐标太大,则被浮层遮挡
                flag = True

            return flag

        except Exception, e:
            print '//--- element %s not exist---//' % element
            print e

    def get_child_count_(self, element):
        start_time = datetime.datetime.now()

        try:
            children = self.web_driver.find_elements_by_id(id_=element)
            end_time = datetime.datetime.now()
            during_time = (end_time - start_time).seconds

            print '//--- finding elements %s within %s seconds---//' % (element, during_time)
            return children.size
        except Exception, e:
            print '//--- elements %s not exist---//' % element
            print e

    def elements_exist_(self, find_element_by='find_element_by_xpath', *args):
        if args == None:
            print 'Page exist'
            return True

    def click_screen(self, x, y, try_time=1, time=None):
        time_.sleep(4)
        width = self.get_size()[0]
        height = self.get_size()[1]

        x1 = float(width * x)
        y1 = float(height * y)

        self.web_driver.tap([(x1, y1)], time)

    def click_coordinate(self, x, y, try_time=1, time=None):
        x1 = float(x)
        y1 = float(y)

        self.web_driver.tap([(x1, y1)], time)

    def swipe(self, start_condition=None, stop_condition=None, direction='L',
              find_element_by_start='find_element_by_xpath',
              find_element_by_stop='find_element_by_xpath', time_swipe=SwipePage_Time, try_time=SwipePage_TryTime):

        args = []
        args_ = []
        count = 0

        size = self.get_size()
        print size
        width = size[0]
        height = size[1]

        offset_length = None
        swipe_from = None

        is_android = re.match("//" + '.*', start_condition) and re.match("//" + '.*', stop_condition) and not (
            re.match("IOS//" + ".*", stop_condition))

        if ('axis' in start_condition) and ('axis' in stop_condition):
            swipe_from = float(start_condition.split('_')[-1])
            offset_length = float(stop_condition.split('_')[-1])

            if direction == 'U':
                if is_android:
                    x1 = float(width * 0.5)
                    y1 = float(height * swipe_from)
                    y2 = y1 - (height * offset_length)
                    args = [x1, y1, x1, y2, time_swipe]
                else:
                    x1 = float(width * 0.5)
                    y1 = float(height * swipe_from)
                    y2 = float(height * -offset_length)
                    args_ = [x1, y1, x1, y2]

            elif direction == 'D':
                if is_android:
                    x1 = float(width * 0.5)
                    y1 = float(height * swipe_from)
                    y2 = y1 + (height * offset_length)
                    args = [x1, y1, x1, y2, time_swipe]
                else:
                    x1 = float(width * 0.5)
                    y1 = float(height * swipe_from)
                    y2 = float(height * offset_length)
                    args_ = [x1, y1, x1, y2]

            elif direction == 'L':
                if is_android:
                    x1 = float(width * swipe_from)
                    y1 = float(height * 0.5)
                    x2 = x1 - (width * offset_length)
                    args = [x1, y1, x2, y1, 500]
                else:
                    x1 = float(width * swipe_from)
                    y1 = float(height * 0.5)
                    x2 = float(width * -offset_length)
                    args_ = [x1, y1, x2, y1]

            elif direction == 'R':
                if is_android:
                    x1 = float(width * swipe_from)
                    y1 = float(height * 0.5)
                    x2 = x1 + (width * offset_length)
                    args = [x1, y1, x2, y1, time_swipe]
                else:
                    x1 = float(width * swipe_from)
                    y1 = float(height * 0.5)
                    x2 = float(width * offset_length)
                    args_ = [x1, y1, x2, y1]

        if 'scroll' in stop_condition:
            scroll_time = stop_condition.split('_')[-1]
            offset_length = '0.06'
            offset_length = float(offset_length) * float(scroll_time)

            if direction == 'U':
                if is_android:
                    x1 = float(width * 0.5)
                    y1 = float(height * 0.95)
                    y2 = y1 - (height * offset_length)
                    args = [x1, y1, x1, y2, time_swipe]
                else:
                    x1 = float(width * 0.5)
                    y1 = float(height * 0.95)
                    y2 = float(height * -offset_length)
                    args_ = [x1, y1, x1, y2, 2000]

            elif direction == 'D':
                if is_android:
                    x1 = float(width * 0.5)
                    y1 = float(height * 0.05)
                    y2 = y1 + (height * offset_length)
                    args = [x1, y1, x1, y2, time_swipe]
                else:
                    x1 = float(width * 0.5)
                    y1 = float(height * 0.05)
                    y2 = float(height * offset_length)
                    args_ = [x1, y1, x1, y2, 1000]

            elif direction == 'L':
                if is_android:
                    x1 = float(width * 0.95)
                    y1 = float(height * 0.5)
                    x2 = x1 - (width * offset_length)
                    args = [x1, y1, x2, y1, 500]
                else:
                    x1 = float(width * 0.95)
                    y1 = float(height * 0.5)
                    x2 = float(width * -offset_length)
                    args_ = [x1, y1, x2, y1, 2000]

            elif direction == 'R':
                if is_android:
                    x1 = float(width * 0.05)
                    y1 = float(height * 0.5)
                    x2 = x1 + (width * offset_length)
                    args = [x1, y1, x2, y1, time_swipe]
                else:
                    x1 = float(width * 0.05)
                    y1 = float(height * 0.5)
                    x2 = float(width * offset_length)
                    args_ = [x1, y1, x2, y1, 2000]

        else:

            if direction == 'U':
                if is_android:
                    x1 = float(Decimal(width * 0.5).quantize(Decimal('0.00')))
                    y1 = float(Decimal(height * 0.5).quantize(Decimal('0.00')))
                    y2 = float(Decimal(height * 0.05).quantize(Decimal('0.00')))
                    args = [x1, y1, x1, y2, time_swipe]
                else:
                    x1 = float(width * 0.5)
                    y1 = float(height * 0.5)
                    # location = self.get_element_location(stop_condition)
                    # y2 = float(location['y'])
                    y2 = float(height * -0.35)
                    args_ = [x1, y1, x1, y2, 1000]

            elif direction == 'D':
                if is_android:
                    x1 = float(width * 0.5)
                    y1 = float(height * 0.5)
                    y2 = float(height * 0.95)
                    args = [x1, y1, x1, y2, time_swipe]
                else:
                    x1 = float(width * 0.5)
                    y1 = float(height * 0.5)
                    y2 = float(height * 0.45)
                    args_ = [x1, y1, x1, y2, 2000]

            elif direction == 'L':
                if is_android:
                    x1 = float(width * 0.95)
                    y1 = float(height * 0.5)
                    x2 = float(width * 0.05)
                    args = [x1, y1, x2, y1, 500]
                else:
                    x1 = float(width * 0.95)
                    y1 = float(height * 0.5)
                    x2 = float(width * -0.9)
                    args_ = [x1, y1, x2, y1, time_swipe]

            elif direction == 'R':
                if is_android:
                    x1 = float(width * 0.05)
                    y1 = float(height * 0.5)
                    x2 = float(width * 0.95)
                    args = [x1, y1, x2, y1, time_swipe]
                else:
                    x1 = float(width * 0.05)
                    y1 = float(height * 0.5)
                    x2 = float(width * 0.9)
                    args_ = [x1, y1, x2, y1, 2000]

        if ('axis' in start_condition) and ('axis' in stop_condition):
            if is_android:
                self.web_driver.swipe(*args)
                return
            else:
                self.web_driver.swipe(*args_)
                return

        if str(stop_condition).__contains__("IOS//"):
            stop_condition = str(stop_condition).split("IOS")[1]

        if self.is_displayed(stop_condition, find_element_by_stop, timeout=5):
            return

        if start_condition == '//':
            pass
        else:
            if not self.element_exist_(start_condition, find_element_by_start):
                raise Exception('start_condition: %s not found !!!, time out: %ss & action_ swipe' % (
                    start_condition, WebDriverWait_TimeOut))

        if 'scroll' in stop_condition:
            if is_android:
                self.web_driver.swipe(*args)
            else:
                self.web_driver.swipe(*args_)
            return

        if len(args) == 0 and len(args_) == 0:
            raise Exception('start/stop condition points is empty. args(android): %s, args_(ios): %s' % (args, args_))
        else:
            if len(args_) != 0:
                args = args_
        print 'args: %s' % args

        while self.web_driver.swipe(*args):
            count += 1
            time.sleep(1.5)
            if is_android:
                if self.element_exist_(stop_condition, find_element_by_stop, timeout=5):
                    return
            else:
                if self.is_displayed(stop_condition, find_element_by_stop):
                    return
            if count == try_time:
                raise Exception('stop_condition: %s not found !!!, time out: %ss & action_ swipe' % (
                    stop_condition, WebDriverWait_TimeOut))

    def click(self, element, find_element_by='find_element_by_xpath'):
        starttime = datetime.datetime.now()

        if '[POP]' in element:
            element = element.split('[POP]')[0]

            if self.element_exist_(element=element, find_element_by=find_element_by, timeout=5):
                target = getattr(self.web_driver, find_element_by)(element)
                target.click()

                endtime = datetime.datetime.now()
                during_time = (endtime - starttime).seconds

                print '//--- finding element %s within %s seconds---//' % (element, during_time)

                print 'with_ %s' % find_element_by
                print 'action_ click'

            return

        if '[UIAKey]' in element:
            element = element.split('[UIAKey]')[1]

            target = getattr(self.web_driver, find_element_by)(element)
            target.click()

            endtime = datetime.datetime.now()
            during_time = (endtime - starttime).seconds

            if int(during_time) < 15:
                print 'finding element %s within %s seconds' % (element, during_time)
            else:
                print '//--- finding element %s within %s seconds---//' % (element, during_time)

            print 'with_ %s' % find_element_by
            print 'action_ click'

            return

        if not self.element_exist_(element, find_element_by):
            raise Exception(
                'element: %s not found !!!, time out: %ss & action_ click & with_ %s' % (
                    element, WebDriverWait_TimeOut, find_element_by))
        else:
            print 'with_ %s' % find_element_by
            print 'action_ click'
            target = getattr(self.web_driver, find_element_by)(element)
            print element
            print target
            self.web_driver.get_screenshot_as_file

            target.click()

    def get_element_location(self, element, find_element_by='find_element_by_xpath', timeout=10):
        starttime = datetime.datetime.now()
        wait = WebDriverWait(self.web_driver, timeout)
        # print self.web_driver.page_source

        try:
            ele = wait.until(lambda x: getattr(x, find_element_by)(element))
            endtime = datetime.datetime.now()
            during_time = (endtime - starttime).seconds

            print '//--- finding element %s within %s seconds---//' % (element, during_time)
            print 'element location: %s' % ele.location
            return ele.location
        except Exception, e:
            print '//--- element %s not exist---//' % element
            print e

    # def axis_click_(self, search_key_word, element_tag, offset_x='0', offset_y='0', UIASwitch='N',
    #                 search_key_word_index=0,find_element_by='find_element_by_xpath',timeout=WebDriverWait_TimeOut, time=None):
    #     starttime = datetime.datetime.now()
    #     wait = WebDriverWait(self.web_driver, timeout)
    #
    #     try:
    #         element = search_key_word.split('_')[0]
    #         ele = wait.until(lambda x: getattr(x, find_element_by)(element))
    #         location=ele.location
    #         size=ele.size
    #         x=location['x']
    #         y=location['y']
    #         click_x=x+float(size['width']*0.78)
    #         click_y=y+float(size['height']*0.55)
    #
    #         self.web_driver.tap([(click_x, click_y)], time)
    #
    #         endtime = datetime.datetime.now()
    #         during_time = (endtime - starttime).seconds
    #
    #         print '//--- finding element %s within %s seconds---//' % (search_key_word, during_time)
    #         print 'element location: %s' % ele.location
    #         return
    #     except Exception, e:
    #         print '//--- element %s not exist---//' % search_key_word
    #         print e


    def axis_click(self, search_key_word, element_tag, offset_x='0', offset_y='0', UIASwitch='N',
                   search_key_word_index=0):
        x_m = None
        y_m = None
        width = self.get_size()[0]
        height = self.get_size()[1]
        POP_TAG = False
        FIND_ELEMENT = False
        if ',' in search_key_word:
            search_key_word = search_key_word.split('_')[0]
        if '[POP]' in search_key_word:
            POP_TAG = True
            search_key_word = search_key_word.split('[POP]')[0]
        if element_tag == 'IOS':
            if self.get_page_value(search_key_word, 'x=', search_key_word_index):
                FIND_ELEMENT = True
                x = self.get_page_value(search_key_word, 'x=', search_key_word_index)
                y = self.get_page_value(search_key_word, 'y=', search_key_word_index)
                h = self.get_page_value(search_key_word, 'height=', search_key_word_index)
                w = self.get_page_value(search_key_word, 'width=', search_key_word_index)
                x_m = float(x) + float(w) / 2 + float(offset_x) * width
                y_m = float(y) + float(h) / 2 + float(offset_y) * height
        if element_tag == 'Android':
            if self.get_page_value(search_key_word, 'bounds', search_key_word_index):
                FIND_ELEMENT = True
                bounds = self.get_page_value(search_key_word, 'bounds', search_key_word_index)
                bounds_prefix = bounds.replace('[', ',')
                bounds_prefix_1 = bounds_prefix.replace(']', ',')
                bounds_prefix_2 = bounds_prefix_1.split(',')
                x0 = bounds_prefix_2[1]
                y0 = bounds_prefix_2[2]
                x1 = bounds_prefix_2[4]
                y1 = bounds_prefix_2[5]
                x_m = float(x0) + (float(x1) - float(x0)) / 2 + float(offset_x) * width
                y_m = float(y0) + (float(y1) - float(y0)) / 2 + float(offset_y) * height
        if FIND_ELEMENT:
            element_xy = str(x_m) + ',' + str(y_m)
            x = float(element_xy.split(',')[0])
            y = float(element_xy.split(',')[1])
            print 'with_ %s, %s' % (x, y)
            print 'action_ click'
            if UIASwitch == 'Y':
                self.click_coordinate(x=x, y=y)
                self.click_coordinate(x=x, y=y)
            else:
                self.click_coordinate(x=x, y=y)
        elif not POP_TAG:
            raise Exception(
                'element: %s not found !!!, time out: %ss & action_ click' % (search_key_word, WebDriverWait_TimeOut))

    # def axis_click(self, search_key_word, element_tag, offset_x='0', offset_y='0', UIASwitch='N',
    #                search_key_word_index=0):
    #     x_m = None
    #     y_m = None
    #
    #     width = self.get_size()[0]
    #     height = self.get_size()[1]
    #
    #     POP_TAG = False
    #     FIND_ELEMENT = False
    #
    #     if ',' in search_key_word:
    #         search_key_word = search_key_word.split('_')[0]
    #
    #     if '[POP]' in search_key_word:
    #         POP_TAG = True
    #         search_key_word = search_key_word.split('[POP]')[0]
    #
    #     if element_tag == 'IOS':
    #         if self.get_page_value(search_key_word, 'x=', search_key_word_index):
    #             FIND_ELEMENT = True
    #
    #             x = offset_x
    #             y = offset_y
    #
    #             h = width
    #             w = height
    #
    #             x_m = float(x) + float(w) / 2 + float(offset_x) * width
    #             y_m = float(y) + float(h) / 2 + float(offset_y) * height
    #
    #     if element_tag == 'Android':
    #         if self.get_page_value(search_key_word, 'bounds', search_key_word_index):
    #             FIND_ELEMENT = True
    #
    #             x = offset_x
    #             y = offset_y
    #
    #             x_m = (float(x) - float(x)) / 2 + float(offset_x) * width
    #             y_m = (float(y) - float(y)) / 2 + float(offset_y) * height
    #
    #     if FIND_ELEMENT:
    #         element_xy = str(x_m) + ',' + str(y_m)
    #
    #         x = float(element_xy.split(',')[0])
    #         y = float(element_xy.split(',')[1])
    #
    #         print 'with_ %s, %s' % (x, y)
    #         print 'action_ click'
    #
    #         self.click_coordinate(x=x, y=y)
    #     else:
    #         if not POP_TAG:
    #             raise Exception(
    #                 'element: %s not found !!!, time out: %ss & action_ click' % (
    #                     search_key_word, WebDriverWait_TimeOut))

    def input(self, element, value, find_element_by='find_element_by_xpath'):

        # if not self.element_exist_(element, find_element_by):
        #     raise Exception(
        #         'element: %s not found !!!, time out: %ss & action_ input_send_keys & value_is_ %s & with_ %s' % (
        #             element, value, WebDriverWait_TimeOut, find_element_by))

        if not isinstance(value, str) and not isinstance(value, unicode):
            raise Exception(
                'be sure the value is str or unicode type !!! & action_ input_send_keys & value_is_ %s' % value)

        print 'with_ %s' % find_element_by
        print 'action_ input_send_keys'
        print 'value_is_ %s' % value
        self.input_send_keys(element, value, find_element_by)

    def input_send_keys(self, element, value, find_element_by='find_element_by_xpath'):

        is_android = re.match("//" + '.*', element) or re.match("xpath_//" + '.*', element)

        if 'IOS' in element:
            element = str(element).split('IOS')[1]

        if not self.element_exist_(element, find_element_by):
            raise Exception(
                'element: %s not found !!!, time out: %ss & action_ input_send_keys & value_is_ %s & with_ %s' % (
                    element, value, WebDriverWait_TimeOut, find_element_by))

        target = getattr(self.web_driver, find_element_by)(element)

        if is_android:
            target.clear()

            if (u'金额' in element) or ('purchase_amt' in element) or (u'份额' in element) or ('pledge' in element) or (
                        'input' in element) or ('cket_loan_repay_crud_money' in element) or (
                        'cket_salary_fin_crud_money' in element) or ('cedt_recharge_amount' in element) or (
                        'et_current_repay_amt' in element) or ('redeem_amt' in element) or (
                        'redeem_product_amt' in element):
                self.secure_keyboard(*value)
                self.secure_keyboard('hide_secure_key_board')
            else:
                # target.send_keys(value)
                if ('请输入手机号码' in element) or ('请输入银行预留手机号码' in element) or ('bind_card_phonenumber' in element) or (
                            '请输入11位手机号码' in element):
                    # handle the mobile input when register
                    # target.send_keys(value[0:3])
                    # target.send_keys(value[3:7])
                    # target.send_keys(value[7:11])
                    cmd = "adb -s %s shell input text %s" % (
                        self.device_id, value[0:3])
                    os.system(cmd)
                    cmd = "adb -s %s shell input text %s" % (
                        self.device_id, value[3:7])
                    os.system(cmd)
                    cmd = "adb -s %s shell input text %s" % (
                        self.device_id, value[7:11])
                    os.system(cmd)

                    # self.web_driver.hide_keyboard()

                    # self./Users/linkinpark/android-sdk-macosx/platform-tools/adb_cmd_call(cmd)
                elif ('请输入您的储蓄卡卡号' in element) or ('请输入您的信用卡卡号' in element):
                    count = 0
                    actual = target.text
                    while (str(actual).replace(" ", "") != str(value)) and count <= 5:
                        target.click()

                        for i in range(0, len(value)):
                            cmd = "adb shell input keyevent KEYCODE_" + \
                                  value[i] + ""

                            os.system(cmd)
                            time.sleep(0.8)

                            if len(str(target.text).replace(" ", "")) > (i + 1):
                                print '长度输入超过预期，需要回删一个字符'
                                cmd = "adb shell input keyevent 67 "
                                os.system(cmd)
                                time.sleep(0.8)

                            if i == len(value) / 2:
                                target.click
                                cmd = "adb shell input keyevent 123 "
                                os.system(cmd)
                                time.sleep(0.8)

                            actual = target.text
                            count += 1

                            if str(actual).replace(" ", "") != value:
                                target.clear

                    if str(actual).replace(" ", "") == value:
                        print 'input value is equal to expected value.'

                        # print 'switch to system default input'
                        # if self.device_id == 'PBV7N16924004496':
                        #     input_method = 'com.android.inputmethod.latin/.LatinIME'
                        # elif self.device_id == 'ac3997d9':
                        #     input_method = 'com.baidu.input_miv6/.ImeService'
                        #
                        # cmd = 'adb shell settings put secure default_input_method %s' % input_method
                        # # cmd = '/Users/linkinpark/android-sdk-macosx/platform-tools/adb shell ime set %s' % input_method
                        # os.system(cmd)
                        #
                        # cmd = "adb -s %s shell input text %s" % (self.device_id, value)
                        # os.system(cmd)
                        #
                        # # self.web_driver.hide_keyboard()
                        # print 'switch back to appium input setting'
                        # cmd = 'adb shell ime set io.appium.android.ime/.UnicodeIME'
                        # os.system(cmd)
                else:
                    target.send_keys(value)

        else:

            if ('请输入您的信用卡卡号' in element) or ('请输入您的储蓄卡卡号' in element) or ('entryPwd' in element) or (
                        u'金额' in element) or (u'份额' in element):
                target.click()
                self.input_press_keycodes_for_ios(*value)

                # hide_secure_key_board = getattr(self.web_driver, 'find_element_by_accessibility_id')('(UIButton_SafeKeyBoard_Hide)')
                # hide_secure_key_board.click()
            else:
                # target.clear()
                # target.set_value(value)
                self.web_driver.set_value(target, value)
                # self.web_driver.hide_keyboard(strategy='tapOutside')

    def input_press_keycodes(self, *args):
        key_code_dict = {'0': 7, '1': 8, '2': 9, '3': 10, '4': 11, '5': 12, '6': 13, '7': 14, '8': 15, '9': 16,
                         '.': 'KEYCODE_LEFT_BRACKET'}
        for arg in args:
            self.web_driver.press_keycode(key_code_dict[arg])

    def input_press_keycodes_for_ios(self, *args):
        for arg in args:
            arg = "[UIAKey]" + arg
            self.click(element=arg, find_element_by='find_element_by_accessibility_id')

    def secure_keyboard(self, *args):
        key_code_dict = {
            '1': [0.125, 0.751], '2': [0.375, 0.751], '3': [0.625, 0.751],
            '4': [0.125, 0.822], '5': [0.375, 0.822], '6': [0.625, 0.822],
            '7': [0.125, 0.893], '8': [0.375, 0.893], '9': [0.625, 0.893],
            '.': [0.125, 0.964], '0': [0.375, 0.964], 'hide_secure_key_board': [0.875, 0.964],
        }

        for arg in args:
            self.click_screen(x=key_code_dict[arg][0], y=key_code_dict[arg][1])

    def perform_actions_(self, *args):

        tag_map_find_element_by = self._tag_map_find_element_by.keys()

        def split_element_prefix(current_arg_prefix):
            prefix = current_arg_prefix.split('_')[0] + '_'
            return prefix

        def split_element_value(current_arg_prefix):
            prefix = current_arg_prefix.split('_')[0] + '_'
            if not prefix in tag_map_find_element_by:
                return current_arg_prefix
            current_arg = current_arg_prefix.split(prefix)[1]
            return current_arg

        def split_element_tag(split_element_prefix, element=''):

            if 'xpath_' in split_element_prefix:
                element_new = split_element_value(element).split('[')[0].split('/')
                element_new_len = element_new.__len__()
                tag = element_new[element_new_len - 1]
                return tag

            else:
                tag = current_arg_prefix.split(split_element_prefix)[1].split('_')[0]
                return tag

        args_len = args.__len__()
        current_len = args_len

        while current_len > 0:

            current_arg_prefix = args[args_len - current_len]

            element_prefix = split_element_prefix(current_arg_prefix)
            element_tag = split_element_tag(element_prefix, current_arg_prefix)

            find_element_by = self._tag_map_find_element_by[element_prefix]

            if element_prefix == 'xpath_':
                current_arg = split_element_value(current_arg_prefix)
            else:
                current_arg = split_element_value(current_arg_prefix).split('_', 1)[1:][0]

            if find_element_by:
                if current_len == 1:
                    getattr(self, self._tag_map_function[element_tag])(current_arg, find_element_by)

                    if current_len == 0:
                        return
                    else:
                        current_len -= 1

                if (args_len - current_len + 1) <= (args_len - 1):
                    current_arg_next_prefix = args[args_len - current_len + 1]
                    current_arg_next = split_element_value(current_arg_next_prefix)
                    element_next_prefix = split_element_prefix(current_arg_next_prefix)

                    is_combination_action = element_next_prefix in ['swipe_']

                    if (re.match(element_prefix + '.*', current_arg_prefix) and re.match(element_next_prefix + '.*',
                                                                                         current_arg_next_prefix)) or is_combination_action:
                        getattr(self, self._tag_map_function[element_tag])(current_arg, find_element_by)

                        if current_len == 0:
                            return
                        else:
                            current_len -= 1

                    else:
                        getattr(self, self._tag_map_function[element_tag])(current_arg, current_arg_next,
                                                                           find_element_by)

                        if current_len == 0:
                            return
                        else:
                            current_len -= 2

                if current_len == 0:
                    return

            else:
                current_arg = split_element_value(split_element_value(current_arg_prefix))

                if element_prefix == 'swipe_':
                    element_prefix_2 = split_element_prefix(split_element_value(current_arg_prefix))
                    find_element_by_start = self._tag_map_find_element_by[element_prefix_2]

                    current_arg_2_prefix = args[args_len - current_len + 1]

                    current_arg_2 = split_element_value(split_element_value(current_arg_2_prefix))
                    element_prefix_2 = split_element_prefix(split_element_value(current_arg_2_prefix))
                    find_element_by_stop = self._tag_map_find_element_by[element_prefix_2]

                    current_arg_3 = args[args_len - current_len + 2]

                    getattr(self, self._tag_map_function[element_prefix])(current_arg, current_arg_2,
                                                                          current_arg_3,
                                                                          find_element_by_start=find_element_by_start,
                                                                          find_element_by_stop=find_element_by_stop)

                    if current_len == 0:
                        return
                    else:
                        current_len -= 3

                if element_prefix == 'axis_':
                    search_key_word = current_arg.split(element_tag + '_')[1]

                    UIASwitch = None
                    index_select = 0

                    if ',' in current_arg.split('_')[-1]:
                        offset_x = current_arg.split(element_tag + '_')[1].split('_')[1].split(',')[0]
                        offset_y = current_arg.split(element_tag + '_')[1].split('_')[1].split(',')[1]
                    elif '[index]' in current_arg.split('_')[-1]:
                        index_select = current_arg.split('[index]')[1]

                        offset_x = '0'
                        offset_y = '0'
                    else:
                        offset_x = '0'
                        offset_y = '0'

                    getattr(self, self._tag_map_function[element_prefix])(search_key_word, element_tag,
                                                                          offset_x=offset_x, offset_y=offset_y,
                                                                          UIASwitch=UIASwitch,
                                                                          search_key_word_index=index_select)

                    if current_len == 0:
                        return
                    else:
                        current_len -= 1

                if element_prefix == 'assert_':
                    search_key_word = current_arg.split(element_tag + '_')[1]
                    expect_value = None
                    assert_attr = None
                    assert_tag = None

                    if '[@' in search_key_word:
                        assert_key = search_key_word.split('[@')[0]
                        if '<=' in search_key_word.split('[@')[1]:
                            assert_tag = '<='
                            assert_attr = search_key_word.split('[@')[1].split(assert_tag)[0]
                            expect_value = search_key_word.split('[@')[1].split('=')[1].split(']')[0]
                        elif '>=' in search_key_word.split('[@')[1]:
                            assert_tag = '>='
                            assert_attr = search_key_word.split('[@')[1].split(assert_tag)[0]
                            expect_value = search_key_word.split('[@')[1].split(assert_tag)[1].split(']')[0]
                        elif '==' in search_key_word.split('[@')[1]:
                            assert_tag = '=='
                            assert_attr = search_key_word.split('[@')[1].split(assert_tag)[0]
                            expect_value = search_key_word.split('[@')[1].split(assert_tag)[1].split(']')[0]
                        elif '=' in search_key_word.split('[@')[1]:
                            assert_tag = '='
                            assert_attr = search_key_word.split('[@')[1].split(assert_tag)[0]
                            expect_value = search_key_word.split('[@')[1].split(assert_tag)[1].split(']')[0]
                        elif '<' in search_key_word.split('[@')[1]:
                            assert_tag = '<'
                            assert_attr = search_key_word.split('[@')[1].split(assert_tag)[0]
                            expect_value = search_key_word.split('[@')[1].split(assert_tag)[1].split(']')[0]
                        elif '>' in search_key_word.split('[@')[1]:
                            assert_tag = '>'
                            assert_attr = search_key_word.split('[@')[1].split(assert_tag)[0]
                            expect_value = search_key_word.split('[@')[1].split(assert_tag)[1].split(']')[0]
                    else:
                        assert_key = search_key_word
                        assert_attr = None
                        expect_value = None

                    assert_result = getattr(self, self._tag_map_function[element_prefix])(assert_key, expect_value,
                                                                                          assert_attr,
                                                                                          assert_tag)

                    if current_len == 0:
                        return assert_result
                    else:
                        current_len -= 1

                if element_prefix == 'getV_':
                    search_key_word_1 = current_arg.split(element_tag + '_')[1].split('[@')[0]
                    if '[index]' in search_key_word_1:
                        search_key_word = search_key_word_1.split('[index]')[0]
                        search_key_word_index = search_key_word_1.split('[index]')[1]
                    else:
                        search_key_word = search_key_word_1
                        search_key_word_index = 0

                    return_key_word = current_arg.split(element_tag + '_')[1].split('[@')[1].split(']')[0]

                    if '_' in return_key_word:
                        return_key_word = return_key_word.split('_')[0]
                        number = True
                    else:
                        return_key_word = return_key_word
                        number = False

                    return getattr(self, self._tag_map_function[element_prefix])(search_key_word, return_key_word,
                                                                                 number, search_key_word_index)

                if current_len == 0:
                    return True

    def get_page_value(self, search_key_word, return_key_word=None, search_key_word_index=0, number=False):
        try:
            cut_1 = str(self.web_driver.page_source).split('>')
        except Exception, e:
            print e

        key_word_index_all = []
        index_select = search_key_word_index
        search_key_word_1 = search_key_word

        if '[index]' in search_key_word:
            search_key_word_1 = search_key_word.split('[index]')[0]
            index_select = search_key_word.split('[index]')[1]

        def key_word_index():
            for i in cut_1:
                # print i
                if search_key_word_1 in i:
                    key_word_index_all.append(cut_1.index(i))

            if not key_word_index_all.__len__() == 0:
                print 'return key word index'
                try:
                    return key_word_index_all[int(index_select)]
                except Exception, e:
                    print e
                    return False

            print 'return false in key_word_index()'
            return False

        def key_word_value():
            j = 1

            for i in cut_2:
                if return_key_word in i:
                    crazystring = i.split('=')[1]
                    print "crazystring = " + crazystring

                    if (cut_2.index(i) + j) <= (cut_2.__len__() - 1):
                        if '="' in cut_2[cut_2.index(i) + 1]:
                            print 'return element text value'
                            if not number:
                                return crazystring
                            else:
                                return crazystring.replace(',', '')

                    while (cut_2.index(i) + j) <= (cut_2.__len__() - 1):
                        if not '="' in cut_2[cut_2.index(i) + j]:
                            crazystring = crazystring + ' ' + cut_2[cut_2.index(i) + j]
                            j += 1
                        else:
                            break

                    print "crazystring = " + crazystring
                    if not number:
                        return crazystring
                    else:
                        return crazystring.replace(',', '')

            print 'return false in key_word_value()'
            return False

        index = key_word_index()

        if index:
            cut_2 = cut_1[index].split(' ')
        else:
            print 'can not find text by key_word_index, return false in get_page_value()'
            return False

        if index and (return_key_word is None):
            print 'return true in get_page_value()'
            return True

        value = key_word_value()

        if value:
            print 'removed " in element text value and return '
            return value.replace('"', '')
        else:
            print 'can not find text by key_word_value, return false in get_page_value()'
            return False

    def assert_value(self, assert_key, expect, assert_attr=None, assert_tag='='):
        assert_key_index = 0
        # crazystring = 'expect'

        # if crazystring:
        #     return True

        if '[index]' in assert_key:
            assert_key_word = assert_key.split('[index]')[0]
            assert_key_index = assert_key.split('[index]')[1]
        else:
            assert_key_word = assert_key

        try:
            crazystring = self.get_page_value(search_key_word=assert_key_word, return_key_word=assert_attr,
                                              search_key_word_index=assert_key_index)
        except:
            raise Exception('can not find assert_value: %s in page !!!' % assert_key_word)

        #
        # if assert_attr is None:
        #     if not self.get_page_value(search_key_word=assert_key_word, return_key_word=assert_attr,
        #                                search_key_word_index=assert_key_index):
        #         raise Exception('can not find assert_value: %s in page !!!' % assert_key_word)
        # else:

        if assert_tag == '=':
            if not expect == crazystring:
                raise Exception(
                    'assert wrong !!! actual: %s, assert_tag: %s, expect: %s' % (crazystring, assert_tag, expect))

        if assert_tag == '==':
            if not expect == crazystring:
                raise Exception(
                    'assert wrong !!! actual: %s, assert_tag: %s, expect: %s' % (crazystring, assert_tag, expect))

        if assert_tag == '>':
            if not expect == crazystring:
                raise Exception(
                    'assert wrong !!! number: %s, assert_tag: %s, expect: %s' % (crazystring, assert_tag, expect))

        if assert_tag == '<':
            if not expect == crazystring:
                raise Exception(
                    'assert wrong !!! number: %s, assert_tag: %s, expect: %s' % (crazystring, assert_tag, expect))

        if assert_tag == '>=':
            if not expect == crazystring:
                raise Exception(
                    'assert wrong !!! number: %s, assert_tag: %s, expect: %s' % (crazystring, assert_tag, expect))

        if assert_tag == '<=':
            if not expect == crazystring:
                raise Exception(
                    'assert wrong !!! number: %s, assert_tag: %s, expect: %s' % (crazystring, assert_tag, expect))

        return True

    def get_value(self, search_key_word, return_key_word, number=False, search_key_word_index=0):
        return self.get_page_value(search_key_word, return_key_word=return_key_word,
                                   search_key_word_index=search_key_word_index,
                                   number=number)

    def adb_cmd_call(self, cmd):
        subprocess.call(cmd, shell=True, executable='/bin/zsh')
