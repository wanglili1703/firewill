# coding: utf-8
import time

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools

SWIPE_START = "swipe_xpath_//android.widget.TextView[@text='银行卡管理']"
SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='绑定银行卡']"
SWIPE_STOP_CONFIRM = "xpath_//android.widget.TextView[@text='绑定银行卡']"

CARD_NO = "xpath_//android.widget.EditText[@text='请输入您的储蓄卡卡号']"
PHONE_NO = "xpath_//android.widget.EditText[@text='请输入银行预留手机号码']"
GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
VERIFY_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入验证码']"
BINDIND_CARD_CONFIRM = "xpath_//android.widget.Button[@text='下一步']"

BINDIND_CARD_DONE = "xpath_//android.widget.Button[@text='确认']"

BANK_CARD_FIRST = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/bankNm']"
BANK_CARD_LAST_CARD_NO = "xpath_//*[contains(@text,'%s')]"
BANK_CARD_OPERATOR = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/ibtn_actionbar_right']"
BANK_CARD_DELETE = "xpath_//android.widget.TextView[@text='删除']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
BANK_CARD_DELETE_CONFIRM = "xpath_//android.widget.Button[@text='确认']"

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
            PHONE_NO, phone_number,
            GET_VERIFY_CODE,
        )

        verification_code = self._db.get_sms_verify_code(mobile=phone_number, template_id='cif_bindBankCard')

        self.perform_actions(
            VERIFY_CODE_INPUT, verification_code,
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
