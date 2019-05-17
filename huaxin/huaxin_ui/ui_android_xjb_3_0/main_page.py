# coding: utf-8
import collections

from _common.page_object import PageObject
from _common.xjb_decorator import dialog_close, dialog_close_afterwards, swipe_guide, robot_log
from huaxin_ui.ui_android_xjb_3_0.home_page import HomePage
import time
import datetime

WELCOME_START = "swipe_xpath_//"
WELCOME_STOP = "swipe_xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/guide_bt']"
WELCOME_STOP_CONFIRM = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/guide_bt']"
# POP_DIALOG_CLOSE = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_dialog_close'][POP]"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
# BACK="xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/login_btn_actionbar_left']"
DIALOG_CLOSE = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_dialog_close']"
FORBBID = "xpath_//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_deny_button'][POP]"

current_page = []


class MainPage(PageObject):
    def __init__(self, web_driver):
        super(MainPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._current_xjb_page = None
        self._ui_flow = []
        self._ui_flow_page = []
        self._ui_flow_page_name = collections.OrderedDict()

    def ui_flow_msg(self):
        print '\r\n'
        print 'ui_flow_is_ '
        for i in self.ui_flow:
            print i

    def __getattr__(self, attribute):

        if hasattr(self._current_xjb_page, attribute):
            attribute_value = getattr(self._current_xjb_page, attribute)

            if callable(attribute_value):
                def wrapper(*args, **kwargs):
                    return_page = attribute_value(*args, **kwargs)

                    if not isinstance(return_page, PageObject):
                        pass
                    else:
                        self._ui_flow.append({return_page.__class__.__name__: return_page})
                        self._ui_flow_page_name.update({return_page.__class__.__name__: return_page})
                        self._ui_flow_page.append(return_page.__class__.__name__)
                        self.current_xjb_page = return_page

                        self.ui_flow_msg()

                    return return_page

                return wrapper

            return attribute_value
        else:
            self.ui_flow_msg()
            raise Exception('%s has no func %s' % (self._current_xjb_page, attribute))

    @property
    def current_xjb_page(self):
        return self._current_xjb_page

    @current_xjb_page.setter
    def current_xjb_page(self, value):
        setattr(value, 'ui_flow', self.ui_flow)
        setattr(value, 'ui_flow_page_name', self.ui_flow_page_name)
        setattr(value, 'ui_flow_page', self.ui_flow_page)
        self._current_xjb_page = value

    @property
    def ui_flow(self):
        return self._ui_flow

    @property
    def ui_flow_page_name(self):
        return self._ui_flow_page_name

    @property
    def ui_flow_page(self):
        return self._ui_flow_page

    @robot_log
    # @dialog_close_afterwards
    # @swipe_guide
    def go_to_home_page(self):
        time.sleep(3)

        self.perform_actions(
            WELCOME_START, WELCOME_STOP, 'L',
            WELCOME_STOP_CONFIRM)
        time.sleep(3)
        print "***********************page_source**********************"
        print self.web_driver.page_source
        if self.element_exist(
                "//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_deny_button']"):
            self.perform_actions(FORBBID)
            # POP_DIALOG_CLOSE

        return_page = HomePage(self.web_driver)

        self._ui_flow.append({return_page.__class__.__name__: return_page})
        self._ui_flow_page_name.update({return_page.__class__.__name__: return_page})
        self._ui_flow_page.append(return_page.__class__.__name__)
        self.current_xjb_page = return_page

        time.sleep(5)
        if self.element_exist("//android.widget.Button[@text='登录']"):
            self.perform_actions(BACK,
                                 DIALOG_CLOSE)

        return self.current_xjb_page


if __name__ == '__main__':
    pass
