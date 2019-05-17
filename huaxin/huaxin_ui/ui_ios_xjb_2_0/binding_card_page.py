# coding: utf-8
import time

from _common.page_object import PageObject
from _common.xjb_decorator import gesture_close_afterwards, user_info_close_afterwards, message_cancel_afterwards, \
    message_i_know_afterwards

from _tools.mysql_xjb_tools import MysqlXjbTools

import huaxin_ui.ui_ios_xjb_2_0.home_page

USER_NAME = "accId_UIATextField_(textField)请输入您的真实的姓名"
ID_NO = "accId_UIATextField_(textField)请输入您的证件号码"
CARD_NO = "accId_UIATextField_(textField)请输入您的储蓄卡卡号"
CARD_TYPE = "accId_UIAStaticText_请选择发卡行"
PHONE_NUMBER = "accId_UIATextField_(textField)请输入银行预留手机号码"
# GET_VERIFY_CODE = "accId_UIAButton_获取验证码"
GET_VERIFY_CODE = "accId_UIAButton_重新获取"
BINDIND_CARD_BLANK = "axis_IOS_btnAuthCode"
VERIFY_CODE_INPUT = "accId_UIATextField_(textField)请输入验证码"
BINDIND_CARD_CONFIRM = "accId_UIAButton_下一步"
BINDIND_CARD_DONE = "accId_UIAButton_先逛逛"

current_page = []


class BindingCardPage(PageObject):
    def __init__(self, web_driver):
        super(BindingCardPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._db = MysqlXjbTools()

    # @message_i_know_afterwards
    # @message_cancel_afterwards
    def binding_card(self, user_name, id_no, band_card_no, phone_number):
        self.perform_actions(USER_NAME, user_name,
                             ID_NO, id_no,
                             CARD_NO, band_card_no,
                             CARD_TYPE,
                             PHONE_NUMBER, phone_number,
                             GET_VERIFY_CODE,
                             )

        verification_code = MysqlXjbTools().get_sms_verify_code(mobile=phone_number, template_id='cif_bindBankCard')

        self.perform_actions(VERIFY_CODE_INPUT, verification_code,
                             BINDIND_CARD_BLANK,
                             BINDIND_CARD_CONFIRM,
                             BINDIND_CARD_DONE,
                             )

        page = huaxin_ui.ui_ios_xjb_2_0.home_page.HomePage(self.web_driver)

        return page
