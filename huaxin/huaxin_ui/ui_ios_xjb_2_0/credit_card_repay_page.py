# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools
from huaxin_ui.ui_ios_xjb_2_0.credit_card_reserved_pay_page import ReservedPayPage

CREDIT_CARD = "axis_IOS_%s"
CREDIT_CARD_CONFIRM = "accId_UIAStaticText_(bankNameLabel)"
CREDIT_CARD_OPERATION = "accId_UIAButton_navMore"
CREDIT_CARD_DELETE = "accId_UIAButton_删除"
TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
CREDIT_CARD_DELETE_CONFIRM = "accId_UIAButton_确认"

ADD_CREDIT_CARD = "accId_UIAButton_添加信用卡"
CREDIT_CARD_NO = "accId_UIATextField_(textField)请输入您的信用卡卡号"
CARD_TYPE = "axis_IOS_手机号"
PHONE_NO = "accId_UIATextField_(textField)请输入银行预留手机号"
GET_VERIFY_CODE = "accId_UIAButton_获取验证码"
VERIFY_CODE_INPUT = "accId_UIATextField_(textField)请输入验证码"
ADD_CREDIT_CARD_CONFIRM = "accId_UIAButton_确定"
ADD_CREDIT_CARD_DONE = "accId_UIAButton_确认"

CREDIT_CARD_SELECTED = "accId_UIAStaticText_(bankName)"
CREDIT_CARD_SELECTED_DETAIL = "accId_UIAStaticText_(bankNameLabel)"
REPAY_AMOUNT = "accId_UIATextField_(textField)请输入还款金额"
REPAY_CONFIRM = "accId_UIAButton_确认"
REPAY_DONE = "accId_UIAButton_确认"

RESERVATION_PAY = "axis_IOS_可预约还款_0.12,0"
CANCEL_RESERVATION = "accId_UIAButton_(UIButton_取消预约)"
CANCEL_RESERVATION_CONFIRM = "axis_IOS_确认"
REPAYMENT_WARN_SET = "axis_IOS_(reminderSettingImageView)"
REPAYMENT_WARN_SWITCH = "axis_IOS_(reminderSwitch)"
# REPAYMENT_WARN_DATE = "xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/lv_filter']"
REPAYMENT_WARN_DATE_COMFIRM = "accId_UIAButton_(UIButton_确定)[POP]"
REPAYMENT_WARN_DATE_CANCEL = "accId_UIAButton_(UIButton_取消)[POP]"

current_page = []


class CreditCardRepayPage(PageObject):
    def __init__(self, web_driver):
        super(CreditCardRepayPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._db = MysqlXjbTools()

    @robot_log
    def delete_credit_card(self, last_card_no, trade_password):
        self.perform_actions(
            CREDIT_CARD % last_card_no,
            CREDIT_CARD_CONFIRM,
            CREDIT_CARD_OPERATION,
            CREDIT_CARD_DELETE,
            TRADE_PASSWORD, trade_password,
            CREDIT_CARD_DELETE_CONFIRM,
        )

        page = self

        return page

    @robot_log
    def add_credit_card(self, credit_card_no, phone_no):
        self.perform_actions(
            ADD_CREDIT_CARD,
            CREDIT_CARD_NO, credit_card_no,
            CARD_TYPE,
            PHONE_NO, phone_no,
            GET_VERIFY_CODE,
        )

        verify_code = self._db.get_sms_verify_code(mobile=phone_no, template_id='credit_bind_card')

        self.perform_actions(
            VERIFY_CODE_INPUT, verify_code,
            ADD_CREDIT_CARD_CONFIRM,
            ADD_CREDIT_CARD_DONE,
        )

        page = self

        return page

    # 信用卡还款
    @robot_log
    def repay(self, repay_amount, trade_password):
        self.perform_actions(CREDIT_CARD_SELECTED,
                             REPAY_AMOUNT, repay_amount,
                             REPAY_CONFIRM,
                             TRADE_PASSWORD, trade_password,
                             REPAY_DONE)
        page = self
        return page

    # 转到预约还款页面
    @robot_log
    def go_to_reserved_pay_page(self):
        self.perform_actions(CREDIT_CARD_SELECTED,
                             RESERVATION_PAY,
                             )

        page = ReservedPayPage(self.web_driver)
        return page

    # 取消预约还款
    @robot_log
    def cancel_reservation(self):
        self.perform_actions(CREDIT_CARD_SELECTED,
                             CANCEL_RESERVATION,
                             CANCEL_RESERVATION_CONFIRM)

        page = ReservedPayPage(self.web_driver)

        return page

    # 添加信用卡还款提醒
    @robot_log
    def add_repayment_warn(self):
        self.perform_actions(CREDIT_CARD_SELECTED,
                             CREDIT_CARD_SELECTED_DETAIL,
                             # REPAYMENT_WARN_SET,
                             REPAYMENT_WARN_SWITCH,
                             # REPAYMENT_WARN_DATE,
                             REPAYMENT_WARN_DATE_COMFIRM,
                             )

    # 取消信用卡还款提醒
    @robot_log
    def cancel_repayment_warn(self):
        self.perform_actions(CREDIT_CARD_SELECTED,
                             CREDIT_CARD_SELECTED_DETAIL,
                             # REPAYMENT_WARN_SET,
                             REPAYMENT_WARN_SWITCH,
                             # REPAYMENT_WARN_DATE,
                             REPAYMENT_WARN_DATE_CANCEL,
                             )
