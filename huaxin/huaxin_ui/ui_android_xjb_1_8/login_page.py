# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log, user_info_close_afterwards, \
    gesture_close_afterwards
import huaxin_ui.ui_android_xjb_2_0.home_page

USER_NAME = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/etAccount']"
PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/etPwd']"
LOGIN_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/login_bt']"
REGISTER_ACCOUNT = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/login_register_bt']"
FORGET_LOGIN_PASSWORD = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/login_forgot_tv']"

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
    @gesture_close_afterwards
    def login(self, user_name, password, return_page):
        self.perform_actions(USER_NAME, user_name,
                             PASSWORD, password,
                             LOGIN_BUTTON,
                             )

        page = self._return_page[return_page]

        return page
