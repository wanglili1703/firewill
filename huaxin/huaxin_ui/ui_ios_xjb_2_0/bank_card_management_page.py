# coding: utf-8
import time

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools

SWIPE_START = "swipe_accId_//"
SWIPE_STOP = "swipe_accId_绑定银行卡"
SWIPE_STOP_CONFIRM = "accId_UIAButton_绑定银行卡"

CARD_NO = "accId_UIATextField_(textField)请输入您的储蓄卡卡号"
CARD_TYPE = "accId_UIAStaticText_请选择发卡行"
PHONE_NO = "accId_UIATextField_(textField)请输入银行预留手机号码"
# GET_VERIFY_CODE = "accId_UIAButton_获取验证码"
GET_VERIFY_CODE = "accId_UIAButton_重新获取"
VERIFY_CODE_INPUT = "accId_UIATextField_(textField)请输入验证码"
BINDIND_CARD_BLANK = "axis_IOS_btnAuthCode"
BINDIND_CARD_CONFIRM = "accId_UIAButton_下一步"

BINDIND_CARD_DONE = "accId_UIAButton_确认"

BANK_CARD_FIRST = "accId_UIAStaticText_(lblBankName)"
BANK_CARD_LAST_CARD_NO = "xpath_//*[contains(@text,'%s')]"
BANK_CARD_OPERATOR = "axis_IOS_UIBarButtonItemLocationRight"
BANK_CARD_DELETE = "accId_UIAButton_删除"
TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
BANK_CARD_DELETE_CONFIRM = "accId_UIAButton_确认"

current_page = []


class BankCardManagementPage(PageObject):
    def __init__(self, web_driver):
        super(BankCardManagementPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._db = MysqlXjbTools()

    @robot_log
    def binding_card(self, band_card_no, phone_number):
        self.perform_actions(
            SWIPE_START, SWIPE_STOP, 'U',
            SWIPE_STOP_CONFIRM,
            CARD_NO, band_card_no,
            CARD_TYPE,
            PHONE_NO, phone_number,
            GET_VERIFY_CODE,
        )

        verification_code = MysqlXjbTools().get_sms_verify_code(mobile=phone_number, template_id='cif_bindBankCard')

        self.perform_actions(
            VERIFY_CODE_INPUT, verification_code,
            BINDIND_CARD_BLANK,
            BINDIND_CARD_CONFIRM,
            BINDIND_CARD_DONE,
        )

        page = self

        return page

    @robot_log
    def delete_band_card(self, trade_password, last_card_no):
        self.perform_actions(
            BANK_CARD_FIRST,
            # BANK_CARD_LAST_CARD_NO % last_card_no,
            BANK_CARD_OPERATOR,
            BANK_CARD_DELETE,
            TRADE_PASSWORD, trade_password,
            BANK_CARD_DELETE_CONFIRM,
        )

        page = self

        return page
