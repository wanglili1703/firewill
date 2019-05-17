# coding: utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page
from _tools.mysql_xjb_tools import MysqlXjbTools

RESERVATION_CODE = "xpathIOS_UIATextField_//UIATextField[@value='请输入收到的预约码']"
RESERVATION_CODE_CONFIRM = "accId_UIAButton_(UIButton_确认)"

USE_OTHER_RESERVATION_CODE = "accId_UIAStaticText_使用其他预约码[POP]"
USE_RESERVATION_CODE = "accId_UIAStaticText_立即使用"

USE_RESERVATION_CODE_COMFIRM = "accId_UIAButton_(UIButton_确认)"
# INPUT_AMOUNT = "accId_UIATextField_(textMoney)"
INPUT_AMOUNT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATableView/UIATableCell/UIATextField"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
USE_RESERVATION_CODE_COMPELETED = "accId_UIAButton_确定[POP]"

BUY_CONTINUE = "accId_UIAButton_继续买入"
MOBILE_CODE = "accId_UIATextField_(textField)"
VIERY_CODE_CONFIRM = "axis_IOS_(textField)_0,0.05"
BUY_DONE = "accId_UIAButton_(confirmButton)[POP]"
HIDE_KEYBOARD = "accId_UIAButton_(UIButton_SafeKeyBoard_Hide)"

current_page = []


class ReservationCodePage(PageObject):
    def __init__(self, web_driver):
        super(ReservationCodePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    # 使用其他预约码
    # flag = 1, 用户自身有预约码, flag = 0, 用户自身没有预约码
    @robot_log
    def use_other_reservation_code(self, reserve_code, trade_password, amount, mobile, flag=0):

        if flag == 1:
            self.assert_values(True, self.element_exist("立即使用", "find_element_by_accessibility_id"))
        else:
            self.assert_values(False, self.element_exist("立即使用", "find_element_by_accessibility_id"))

        self.perform_actions(
            USE_OTHER_RESERVATION_CODE,
            RESERVATION_CODE, reserve_code,
            RESERVATION_CODE_CONFIRM,
            INPUT_AMOUNT, amount,
            HIDE_KEYBOARD,
            USE_RESERVATION_CODE_COMFIRM,
        )

        if self.element_exist(u'风险提示', 'find_element_by_accessibility_id'):
            self.perform_actions(
                BUY_CONTINUE,
            )

            verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile, template_id='as_risk_level')

            self.perform_actions(
                MOBILE_CODE, verify_code,
                VIERY_CODE_CONFIRM,
                TRADE_PASSWORD, trade_password,
                BUY_DONE,
            )

        else:
            self.perform_actions(
                TRADE_PASSWORD, trade_password,
                # USE_RESERVATION_CODE_COMPELETED
            )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page

    # 使用自己的预约码
    @robot_log
    def use_reservation_code(self, trade_password, amount, mobile):
        self.perform_actions(
            USE_RESERVATION_CODE,
            INPUT_AMOUNT, amount,
            HIDE_KEYBOARD,
            USE_RESERVATION_CODE_COMFIRM,
        )

        if self.element_exist(u'风险提示', 'find_element_by_accessibility_id'):
            self.perform_actions(
                BUY_CONTINUE,
            )

            verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile, template_id='as_risk_level')

            self.perform_actions(
                MOBILE_CODE, verify_code,
                VIERY_CODE_CONFIRM,
                TRADE_PASSWORD, trade_password,
                BUY_DONE,
            )

        else:
            self.perform_actions(
                TRADE_PASSWORD, trade_password,
                # USE_RESERVATION_CODE_COMPELETED,
            )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page
