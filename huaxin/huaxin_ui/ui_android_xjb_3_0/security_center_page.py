# coding: utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_android_xjb_3_0.setting_login_password_page import SettingLoginPasswordPage
from huaxin_ui.ui_android_xjb_3_0.setting_modify_mobile_page import SettingModifyMobilePage
from huaxin_ui.ui_android_xjb_3_0.security_center_trade_password_page import SecurityCenterTradePasswordPage
import huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page
import huaxin_ui.ui_android_xjb_3_0.login_record_page
import huaxin_ui.ui_android_xjb_3_0.personal_setting_page
import huaxin_ui.ui_android_xjb_3_0.login_mode_page
import time

LOGIN_PASSWORD_BUTTON = "xpath_//android.widget.TextView[@text='登录密码']"
TRADE_PASSWORD_BUTTON = "xpath_//android.widget.TextView[@text='交易密码']"
CHANGE_PHONE_BUTTON = "xpath_//android.widget.TextView[@text='修改绑定手机']"
SWIPE_BEGIN = "swipe_xpath_//"
LOGIN_RECORD_STOP = "swipe_xpath_//android.widget.TextView[@text='登录记录']"
LOGIN_RECORD = "xpath_//android.widget.TextView[@text='登录记录']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
LOGIN_MODE = "xpath_//android.widget.TextView[@text='登录方式']"

current_page = []


class SecurityCenterPage(PageObject):
    def __init__(self, web_driver):
        super(SecurityCenterPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('安全中心', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def go_to_setting_login_password_page(self):
        self.perform_actions(LOGIN_PASSWORD_BUTTON)
        page = SettingLoginPasswordPage(self.web_driver)

        return page

    # 可删除
    @robot_log
    def go_to_setting_trade_password_page(self):
        self.perform_actions(TRADE_PASSWORD_BUTTON)
        page = huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page.SettingTradePasswordPage(self.web_driver)

        return page

    # @robot_log
    # def go_to_setting_modify_mobile_page(self, device_id):
    #     time.sleep(3)
    #     self.perform_actions(CHANGE_PHONE_BUTTON)
    #     page = SettingModifyMobilePage(self.web_driver, device_id)
    #
    #     return page

    @robot_log
    def go_to_security_center_trade_password_page(self):
        self.perform_actions(TRADE_PASSWORD_BUTTON)
        page = SecurityCenterTradePasswordPage(self.web_driver)

        return page

    @robot_log
    def go_to_login_record_page(self):
        self.perform_actions(SWIPE_BEGIN, LOGIN_RECORD_STOP, 'U')
        self.perform_actions(LOGIN_RECORD)

        page = huaxin_ui.ui_android_xjb_3_0.login_record_page.LoginRecordPage(self.web_driver)
        return page

    @robot_log
    def back_to_personal_setting_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.personal_setting_page.PersonalSettingPage(self.web_driver)
        return page

    @robot_log
    def go_to_login_mode_page(self):
        self.perform_actions(LOGIN_MODE)

        page = huaxin_ui.ui_android_xjb_3_0.login_mode_page.LoginModePage(self.web_driver)
        return page
