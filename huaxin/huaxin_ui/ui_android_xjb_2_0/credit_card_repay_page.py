# coding=utf-8
import time
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools
from huaxin_ui.ui_android_xjb_2_0.credit_card_reserved_pay_page import ReservedPayPage

CREDIT_CARD = "xpath_//*[contains(@text,%s)]"
CREDIT_CARD_CONFIRM = "xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/ccv_credit_repayment']"
CREDIT_CARD_OPERATION = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/ibtn_actionbar_right']"
CREDIT_CARD_DELETE = "xpath_//android.widget.TextView[@text='删除']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
CREDIT_CARD_DELETE_CONFIRM = "xpath_//android.widget.Button[@text='确认']"

CREDIT_CARD_SELECTED = "xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/rl_credit_item']"
REPAY_AMOUNT = "xpath_//android.widget.EditText[@text='请输入还款金额']"
REPAY_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
REPAY_DONE = "xpath_//android.widget.Button[@text='确认']"
RESERVATION_PAY = "axis_Android_可预约还款_0.12,0"
CANCEL_RESERVATION = "xpath_//android.widget.TextView[@text='取消预约']"
CANCEL_RESERVATION_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
REPAYMENT_WARN_SET = "xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/ccv_credit_repayment']"
REPAYMENT_WARN_SWITCH = "xpath_//android.widget.ToggleButton[@resource-id='com.shhxzq.xjb:id/repayment_warn_switch']"
REPAYMENT_WARN_DATE = "xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/lv_filter']"
REPAYMENT_WARN_DATE_COMPELETED = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_compeleted']"

ADD_CREDIT_CARD = "xpath_//android.widget.TextView[@text='添加信用卡']"
CREDIT_CARD_NO = "xpath_//android.widget.EditText[@text='请输入您的信用卡卡号']"
PHONE_NO = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/bind_card_phonenumber']"
GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
INPUT_VERIFY_CODE = "xpath_//android.widget.EditText[@text='请输入验证码']"
ADD_CREDIT_CARD_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/bind_card_sure_bt']"
ADD_CREDIT_CARD_DONE = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/useroperation_succeed_bt']"

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
            PHONE_NO, phone_no,
            GET_VERIFY_CODE,
        )

        verify_code = MysqlXjbTools().get_sms_verify_code(mobile=phone_no, template_id='credit_bind_card')

        self.perform_actions(
            INPUT_VERIFY_CODE, verify_code,
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
                             REPAYMENT_WARN_SET,
                             REPAYMENT_WARN_SWITCH,
                             REPAYMENT_WARN_DATE,
                             REPAYMENT_WARN_DATE_COMPELETED
                             )

    # 添加信用卡还款提醒
    @robot_log
    def cancel_repayment_warn(self):
        self.perform_actions(CREDIT_CARD_SELECTED,
                             REPAYMENT_WARN_SET,
                             REPAYMENT_WARN_SWITCH
                             )
