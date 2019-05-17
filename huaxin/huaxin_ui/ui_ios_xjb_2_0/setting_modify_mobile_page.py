# coding: utf-8
import time
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools
from huaxin_ui.ui_ios_xjb_2_0.login_page import LoginPage

TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
TRADE_PASSWORD_CONFIRM = "accId_UIAButton_确认"

RECEIVE_SMS = "accId_UIAStaticText_能接收短信"

GET_VERIFY_CODE = "accId_UIAButton_获取验证码"
TRADE_PASSWORD_VERIFY_CODE_INPUT = "accId_UIATextField_(textField)请输入验证码"
VERIFY_CODE_CONFIRM = "accId_UIAButton_提交"

MOBILE = "accId_UIATextField_(textField)请输入11位手机号码"
MOBILE_GET_VERIFY_CODE = "accId_UIAButton_获取验证码"
MOBILE_VERIFY_CODE_INPUT = "accId_UIATextField_(textField)请输入验证码"
MOBILE_CONFIRM = "accId_UIAButton_确认"

MODIFY_MOBILE_DONE = "accId_UIAButton_确认"

current_page = []


class SettingModifyMobilePage(PageObject):
    def __init__(self, web_driver):
        super(SettingModifyMobilePage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._db = MysqlXjbTools()

    @robot_log
    def modify_mobile(self, mobile_old, trade_password, mobile_new):
        self.perform_actions(
            TRADE_PASSWORD, trade_password,
            # TRADE_PASSWORD_CONFIRM,
            RECEIVE_SMS,
            GET_VERIFY_CODE,
        )

        verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile_old, template_id='cif_changeMobile')

        self.perform_actions(
            TRADE_PASSWORD_VERIFY_CODE_INPUT, verify_code,
            VERIFY_CODE_CONFIRM,
            MOBILE, mobile_new,
            MOBILE_GET_VERIFY_CODE,
        )

        verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile_new, template_id='cif_changeMobile')

        self.perform_actions(
            MOBILE_VERIFY_CODE_INPUT, verify_code,
            MOBILE_CONFIRM,
            MODIFY_MOBILE_DONE,
        )

        page = LoginPage(self.web_driver)

        return page
