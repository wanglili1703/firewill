# coding: utf-8
import time

from _common.page_object import PageObject
from _common.xjb_decorator import gesture_close_afterwards, user_info_close_afterwards

from _tools.mysql_xjb_tools import MysqlXjbTools

import huaxin_ui.ui_android_xjb_2_0.home_page

USER_NAME = "xpath_//android.widget.EditText[@text='请输入您本人的姓名']"
ID_NO = "xpath_//android.widget.EditText[@text='请输入您的证件号码']"
CARD_NO = "xpath_//android.widget.EditText[@text='请输入您的储蓄卡卡号']"
PHONE_NUMBER = "xpath_//android.widget.EditText[@text='请输入银行预留手机号码']"
GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
VERIFY_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入验证码']"
BINDIND_CARD_CONFIRM = "xpath_//android.widget.Button[@text='下一步']"
BINDIND_CARD_DONE = "xpath_//android.widget.TextView[@text='先逛逛']"

current_page = []


class BindingCardPage(PageObject):
    def __init__(self, web_driver):
        super(BindingCardPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._db = MysqlXjbTools()

    @user_info_close_afterwards
    @gesture_close_afterwards
    def binding_card(self, user_name, id_no, band_card_no, phone_number):
        self.perform_actions(USER_NAME, user_name,
                             ID_NO, id_no,
                             CARD_NO, band_card_no,
                             PHONE_NUMBER, phone_number,
                             GET_VERIFY_CODE,
                             )

        verification_code = MysqlXjbTools().get_sms_verify_code(mobile=phone_number, template_id='cif_bindBankCard')

        self.perform_actions(VERIFY_CODE_INPUT, verification_code,
                             BINDIND_CARD_CONFIRM,
                             BINDIND_CARD_DONE,
                             )

        page = huaxin_ui.ui_android_xjb_2_0.home_page.HomePage(self.web_driver)

        return page
