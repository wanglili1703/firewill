# coding: utf-8
import time

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

from _tools.mysql_xjb_tools import MysqlXjbTools

import huaxin_ui.ui_ios_xjb_3_0.home_page
import huaxin_ui.ui_ios_xjb_3_0.binding_card_complete_page

# USER_NAME = "accId_UIATextField_(textField)请输入您的真实的姓名"
USER_NAME = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATableView/UIATableCell/UIATextField"
# ID_NO = "accId_UIATextField_(textIdNo)"
ID_NO = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATableView/UIATableCell[3]/UIATextField"
# CARD_NO = "accId_UIATextField_(textCardNo)请输入您的储蓄卡卡号"
CARD_NO = "xpathIOS_UIATextField_IOS//UIATableCell/UIATextField[@value='请输入您的储蓄卡卡号']"
# CARD_NO = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATableView/UIATableCell[4]/UIATextField"
CARD_TYPE = "accId_UIAStaticText_选择发卡行"
ID_TYPE = "accId_UIATableCell_(IDType)"
# PHONE_NUMBER = "accId_UIATextField_(textMobileNo)请输入银行预留手机号码"
PHONE_NUMBER = "xpathIOS_UIATextField_//UIAStaticText[@label='手机号']/following-sibling::UIATextField[1]"
GET_VERIFY_CODE = "accId_UIAButton_(UIButton_获取验证码)"
# GET_VERIFY_CODE = "accId_UIAButton_(UIButton_重新获取)"
# BINDIND_CARD_BLANK = "axis_IOS_(btnGetAuthCode)"
VERIFY_CODE_INPUT = "xpathIOS_UIATextField_//UIAStaticText[@label='验证码']/following-sibling::UIATextField[1]"
# VERIFY_CODE_INPUT = "accId_UIATextField_(textVerifyCodeNo)请输入验证码"
BINDIND_CARD_CONFIRM = "accId_UIAButton_(UIButton_确定)"
SWIPE_BEGIN = "swipe_accId_(验证码)"
SWIPE_BINDIND_CARD_CONFIRM = "swipe_accId_(UIButton_确定)"
BINDIND_CARD_DONE = "accId_UIAButton_先逛逛"
FINISH = "accId_UIAButton_完成"

KEYBOARD_RETURN = "accId_UIAButton_Return"

current_page = []


class BindingCardPage(PageObject):
    def __init__(self, web_driver):
        super(BindingCardPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._db = MysqlXjbTools()

    @robot_log
    def verify_at_binding_card_page(self):
        self.assert_values("绑定银行卡", self.get_text("//UIAStaticText[@label='绑定银行卡']"))

        page = self
        return page

    @robot_log
    def binding_card(self, user_name, id_no, bank_card_no, phone_number):
        self.perform_actions(
            # USER_NAME, user_name,
            #                  ID_TYPE,
            #                  FINISH,
            #                  ID_NO, id_no,
            CARD_NO, bank_card_no,
            # CARD_TYPE,
        )

        self.perform_actions(
            PHONE_NUMBER, phone_number,
            GET_VERIFY_CODE
        )

        verification_code = MysqlXjbTools().get_sms_verify_code(mobile=phone_number, template_id='cif_bindBankCard')

        self.perform_actions(VERIFY_CODE_INPUT, verification_code,
                             KEYBOARD_RETURN,
                             # SWIPE_BEGIN, SWIPE_BINDIND_CARD_CONFIRM, 'U',
                             BINDIND_CARD_CONFIRM
                             )

        page = huaxin_ui.ui_ios_xjb_3_0.binding_card_complete_page.BindingCardCompletePage(self.web_driver)

        return page
