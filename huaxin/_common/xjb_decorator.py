# coding: utf-8

from functools import wraps

import time
from robot.api import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from _common.global_config import GlobalConfig

WELCOME_START = "swipe_xpath_//"
WELCOME_STOP = "swipe_xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/guide_bt']"
WELCOME_STOP_CONFIRM = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/guide_bt']"

GESTURE = "xpath_//android.widget.TextView[@text='取消'][POP]"
PERMISSION_CLOSE="xpath_//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button'][POP]"
USER_INFO = "xpath_//android.widget.Button[@text='我知道了'][POP]"
DIALOG = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_dialog_close']"

MESSAGE_CANCEL = "accId_UIAButton_取消"
MESSAGE_I_KNOW = "accId_UIAButton_我知道了"

def gesture_close_afterwards(func):
    @wraps(func)
    def wrapper(page_obj, *args, **kwargs):
        return_page = func(page_obj, *args, **kwargs)
        page_obj.perform_actions(GESTURE)
        page_obj.perform_actions(PERMISSION_CLOSE)


        return return_page

    return wrapper


def user_info_close_afterwards(func):
    @wraps(func)
    def wrapper(page_obj, *args, **kwargs):
        return_page = func(page_obj, *args, **kwargs)
        page_obj.perform_actions(USER_INFO)

        return return_page

    return wrapper


def dialog_close(func):
    @wraps(func)
    def wrapper(page_obj, *args, **kwargs):
        try:
            button = page_obj.web_driver.find_element_by_xpath(
                "//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_dialog_close']")
            button.click()
        except NoSuchElementException:
            pass

        return_page = func(page_obj, *args, **kwargs)

        return return_page

    return wrapper


def dialog_close_afterwards(func):
    @wraps(func)
    def wrapper(page_obj, *args, **kwargs):
        return_page = func(page_obj, *args, **kwargs)
        page_obj.perform_actions(DIALOG)

        return return_page

    return wrapper


def robot_log(func):
    @wraps(func)
    def wrapper(page_obj, *args, **kwargs):
        logger.info(func.__name__)
        if args.__len__() > 0:
            logger.info(args)

        return_page = func(page_obj, *args, **kwargs)

        logger.info('return page is %s' % return_page)
        time.sleep(1)
        page_obj.screen_shot()

        return return_page

    return wrapper


def swipe_guide(func):
    @wraps(func)
    def wrapper(page_obj, *args, **kwargs):
        page_obj.perform_actions(WELCOME_START, WELCOME_STOP, 'L',
                                 WELCOME_STOP_CONFIRM,
                                 )
        return_page = func(page_obj, *args, **kwargs)
        return return_page

    return wrapper


# for ios

def message_cancel_afterwards(func):
    @wraps(func)
    def wrapper(page_obj, *args, **kwargs):
        return_page = func(page_obj, *args, **kwargs)

        try:
            button = page_obj.web_driver.find_element_by_accessibility_id('取消')
            button.click()
        except NoSuchElementException:
            pass

        return return_page

    return wrapper


def message_i_know_afterwards(func):
    @wraps(func)
    def wrapper(page_obj, *args, **kwargs):
        return_page = func(page_obj, *args, **kwargs)

        try:
            button = page_obj.web_driver.find_element_by_accessibility_id('(UIButton_)')
            button.click()
        except Exception:
            pass

        return return_page

    return wrapper


def message_dialog_close(func):
    @wraps(func)
    def wrapper(page_obj, *args, **kwargs):
        try:
            button = page_obj.web_driver.find_element_by_accessibility_id("(UIButton_delete)")
            button.click()
        except NoSuchElementException:
            pass

        return_page = func(page_obj, *args, **kwargs)

        return return_page

    return wrapper
