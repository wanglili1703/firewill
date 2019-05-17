# coding: utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_2_0.setting_login_password_page import SettingLoginPasswordPage
from huaxin_ui.ui_ios_xjb_2_0.setting_modify_mobile_page import SettingModifyMobilePage
from huaxin_ui.ui_ios_xjb_2_0.setting_trade_password_page import SettingTradePasswordPage

LOGIN_PASSWORD_BUTTON = "accId_UIAStaticText_登录密码"
TRADE_PASSWORD_BUTTON = "accId_UIAStaticText_交易密码"
CHANGE_PHONE_BUTTON = "accId_UIAStaticText_修改绑定手机"

current_page = []


class SecurityCenterPage(PageObject):
    def __init__(self, web_driver):
        super(SecurityCenterPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_setting_login_password_page(self):
        self.perform_actions(LOGIN_PASSWORD_BUTTON)
        page = SettingLoginPasswordPage(self.web_driver)

        return page

    @robot_log
    def go_to_setting_trade_password_page(self):
        self.perform_actions(TRADE_PASSWORD_BUTTON)
        page = SettingTradePasswordPage(self.web_driver)

        return page

    @robot_log
    def go_to_setting_modify_mobile_page(self):
        self.perform_actions(CHANGE_PHONE_BUTTON)
        page = SettingModifyMobilePage(self.web_driver)

        return page
