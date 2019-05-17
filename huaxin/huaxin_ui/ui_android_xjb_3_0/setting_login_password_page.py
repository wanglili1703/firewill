# coding: utf-8
from _common.page_object import PageObject
import huaxin_ui.ui_android_xjb_3_0.login_page
from _common.xjb_decorator import robot_log

FIND_LOGIN_PASSWORD = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_account_find_pwd']"
MODIFY_LOGIN_PASSWORD = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_account_modify_pwd']"
CURRENT_LOGIN_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cedt_modify_current_pwd']"
CURRENT_LOGIN_PASSWORD_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_modify_next']"
SETTING_LOGIN_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cedt_modify_pwd_confirm']"
SETTING_LOGIN_PASSWORD_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_modify_confirm']"
SETTING_LOGIN_PASSWORD_AGAIN = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cedt_modify_pwd_confirm']"
SETTING_LOGIN_PASSWORD_AGAIN_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_modify_confirm']"

current_page = []


class SettingLoginPasswordPage(PageObject):
    def __init__(self, web_driver):
        super(SettingLoginPasswordPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def modify_login_password(self, login_password_old, login_password_new):
        self.perform_actions(
            MODIFY_LOGIN_PASSWORD,
            CURRENT_LOGIN_PASSWORD, login_password_old,
            CURRENT_LOGIN_PASSWORD_CONFIRM,
            SETTING_LOGIN_PASSWORD, login_password_new,
            SETTING_LOGIN_PASSWORD_CONFIRM,
            SETTING_LOGIN_PASSWORD_AGAIN, login_password_new,
            SETTING_LOGIN_PASSWORD_AGAIN_CONFIRM,
        )

        page = huaxin_ui.ui_android_xjb_3_0.login_page.LoginPage(self.web_driver)

        return page

    @robot_log
    def find_login_password(self):
        pass
