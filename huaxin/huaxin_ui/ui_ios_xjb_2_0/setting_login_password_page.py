# coding: utf-8
from _common.page_object import PageObject
import huaxin_ui.ui_ios_xjb_2_0.login_page
from _common.xjb_decorator import robot_log

FIND_LOGIN_PASSWORD = "accId_UIAElement_找回登录密码"
MODIFY_LOGIN_PASSWORD = "accId_UIAElement_修改登录密码"
CURRENT_LOGIN_PASSWORD = "accId_UIASecureTextField_(textField)当前登录密码"
CURRENT_LOGIN_PASSWORD_CONFIRM = "accId_UIAButton_下一步"
SETTING_LOGIN_PASSWORD = "accId_UIASecureTextField_(textField)8-20位字母,数字或符号任意两种组合"
SETTING_LOGIN_PASSWORD_CONFIRM = "accId_UIAButton_下一步"
SETTING_LOGIN_PASSWORD_AGAIN = "accId_UIASecureTextField_(textField)8-20位字母,数字或符号任意两种组合"
SETTING_LOGIN_PASSWORD_AGAIN_CONFIRM = "accId_UIAButton_确认"

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
            # SETTING_LOGIN_PASSWORD_AGAIN, login_password_new,
            # SETTING_LOGIN_PASSWORD_AGAIN_CONFIRM,
        )

        page = huaxin_ui.ui_ios_xjb_2_0.login_page.LoginPage(self.web_driver)

        return page

    @robot_log
    def find_login_password(self):
        pass
