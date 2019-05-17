# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log, user_info_close_afterwards, \
    gesture_close_afterwards, dialog_close_afterwards
from huaxin_ui.ui_android_xjb_2_0.register_page import RegisterPage

import huaxin_ui.ui_android_xjb_2_0.home_page

USER_NAME = "xpath_//android.widget.EditText[@text='请输入手机']"
PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/etPwd']"
LOGIN_BUTTON = "xpath_//android.widget.Button[@text='登录']"
REGISTER_ACCOUNT = "xpath_//android.widget.TextView[@text='注册账户']"
FORGET_LOGIN_PASSWORD = "xpath_//android.widget.TextView[@text='忘记密码？']"

POP_CANCEL = "xpath_//android.widget.TextView[@text='取消']"
POP_DIALOG_CLOSE = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_dialog_close'][POP]"

current_page = []


class LoginPage(PageObject):
    def __init__(self, web_driver):
        super(LoginPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
            'HomePage': huaxin_ui.ui_android_xjb_2_0.home_page.HomePage(self.web_driver)
        }

    @robot_log
    @user_info_close_afterwards
    # @dialog_close_afterwards
    # @gesture_close_afterwards
    def login(self, user_name, password, return_page):
        self.perform_actions(USER_NAME, user_name,
                             PASSWORD, password,
                             LOGIN_BUTTON,
                             POP_CANCEL,
                             POP_DIALOG_CLOSE,
                             )

        page = self._return_page[return_page]

        return page

    @robot_log
    def go_to_register_page(self):
        self.perform_actions(REGISTER_ACCOUNT)
        page = RegisterPage(self.web_driver)
        return page
