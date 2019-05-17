# coding=utf-8
import decimal

import time

from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools
from huaxin_ui.ui_ios_xjb_3_0.credit_card_reserved_pay_page import ReservedPayPage
import huaxin_ui.ui_ios_xjb_3_0.credit_card_add_finish_page
import huaxin_ui.ui_ios_xjb_3_0.credit_card_repay_record_page
import huaxin_ui.ui_ios_xjb_3_0.binding_card_page

CREDIT_CARD = "accId_UIAStaticText_(**** **** **** %s)"
CREDIT_CARD_CONFIRM = "accId_UIAStaticText_(信用卡 | 尾号%s)"
CREDIT_CARD_OPERATION = "accId_UIAButton_(UIButton_navMore.png)"
CREDIT_CARD_DELETE = "accId_UIAButton_删除"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
CREDIT_CARD_DELETE_CONFIRM = "accId_UIAButton_(UIButton_确认)"

ADD_CREDIT_CARD = "accId_UIAButton_(UIButton_+ 添加信用卡)"
CREDIT_CARD_NO = "xpathIOS_UIATextField_IOS//UIATextField[@value='请输入您的信用卡卡号']"
CARD_TYPE = "axis_IOS_手机号"
# PHONE_NO = "accId_UIATextField_(textField)请输入银行预留手机号"
PHONE_NO = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIAScrollView/UIATextField[4]"
GET_VERIFY_CODE = "accId_UIAButton_(UIButton_获取验证码)"
VERIFY_CODE_INPUT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIAScrollView/UIATextField[5]"
ADD_CREDIT_CARD_CONFIRM = "accId_UIAButton_(UIButton_确定)"
ADD_CREDIT_CARD_DONE = "accId_UIAButton_(UIButton_确定)"

CREDIT_CARD_SELECTED = "accId_UIAStaticText_信用卡"
CREDIT_CARD_SELECTED_DETAIL = "xpathIOS_UIAStaticText_//UIAStaticText[contains(@label, '银行')]"
REPAY_AMOUNT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
REPAY_CONFIRM = "accId_UIAButton_(UIButton_确认)"
REPAY_DONE = "accId_UIAButton_(UIButton_确定)"

RESERVATION_PAY = "axis_IOS_可预约还款_0.12,0"
CANCEL_RESERVATION = "accId_UIAButton_(UIButton_取消预约)"
# CANCEL_RESERVATION_CONFIRM = "axis_IOS_(UIButton_确认)"
CANCEL_RESERVATION_CONFIRM = "xpathIOS_UIAButton_//UIACollectionCell/UIAButton[@label='确认']"
REPAYMENT_WARN_SET = "axis_IOS_(reminderSettingImageView)"
REPAYMENT_WARN_SWITCH = "xpathIOS_UIASwitch_//UIASwitch"
# REPAYMENT_WARN_DATE = "xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/lv_filter']"
REPAYMENT_WARN_DATE_CONFIRM = "accId_UIAButton_(UIButton_确定)[POP]"
REPAYMENT_WARN_DATE_CANCEL = "accId_UIAButton_(UIButton_取消)[POP]"

BACK = "accId_UIAButton_UIBarButtonItemLocationRight"

USE_COUPON = "axis_IOS_优惠券_0.5,0"
COUPON = "accId_UIAStaticText_满10减1所有产品不可叠加"
NON_SUPER_COMPOSED_COUPON_SWIPE_STOP = "swipe_accId_满10减1所有产品不可叠加"
COUPON_CONFIRM = "accId_UIAButton_(UIButton_确定)"
CREDIT_SELECT = "xpathIOS_UIAStaticText_//UIAStaticText[contains(@name, '**** **** **** %s')]"
RECORD = "accId_UIAButton_还款记录"
BANK_NAME = "/AppiumAUT/UIAApplication/UIAWindow/UIAStaticText[1]"
TIPS_CONFIRM = "accId_UIAButton_(UIButton_确定)"

current_page = []


class CreditCardRepayPage(PageObject):
    def __init__(self, web_driver):
        super(CreditCardRepayPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_credit_card_repay_page(self):
        self.assert_values("信用卡还款", self.get_text("//UIAStaticText[@label='信用卡还款']"))

    @robot_log
    def verify_at_credit_card_list_page(self):
        self.assert_values("我的信用卡", self.get_text("//UIAStaticText[@label='我的信用卡']"))

        page = self
        return page

    @robot_log
    def delete_credit_card(self, last_card_no, trade_password):
        self.perform_actions(
            CREDIT_CARD % last_card_no)

        if self.element_exist("(UIButton_取消预约)", "find_element_by_accessibility_id"):
            self.perform_actions(CANCEL_RESERVATION,
                                 CANCEL_RESERVATION_CONFIRM)
        self.perform_actions(
            CREDIT_CARD_CONFIRM % last_card_no,
            CREDIT_CARD_OPERATION,
            CREDIT_CARD_DELETE,
            TRADE_PASSWORD, trade_password,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.credit_card_add_finish_page.CreditCardAddFinishPage(self.web_driver)

        return page

    @robot_log
    def add_credit_card(self, credit_card_no, phone_no):
        self.perform_actions(
            ADD_CREDIT_CARD,
            CREDIT_CARD_NO, credit_card_no,
            # CARD_TYPE,
            PHONE_NO, phone_no,
            GET_VERIFY_CODE,
        )

        _db = MysqlXjbTools()
        verify_code = _db.get_sms_verify_code(mobile=phone_no, template_id='credit_bind_card')

        self.perform_actions(
            VERIFY_CODE_INPUT, verify_code,
            ADD_CREDIT_CARD_CONFIRM
        )

        page = huaxin_ui.ui_ios_xjb_3_0.credit_card_add_finish_page.CreditCardAddFinishPage(self.web_driver)

        return page

    @robot_log
    def select_credit_card(self, last_card_no):
        self.perform_actions(CREDIT_SELECT % last_card_no)

        page = self
        return page

    @robot_log
    def go_to_credit_repay_record_page(self):
        self.perform_actions(RECORD)

        page = huaxin_ui.ui_ios_xjb_3_0.credit_card_repay_record_page.CreditCardRepayRecordPage(self.web_driver)
        return page

    # 信用卡还款
    @robot_log
    def repay(self, repay_amount, trade_password, non_superposed_coupon=None):
        self.perform_actions(CREDIT_CARD_SELECTED,
                             REPAY_AMOUNT, repay_amount
                             )

        bank = self.get_text(BANK_NAME)
        ASSERT_DICT.update({
            "bank": bank
        })

        if non_superposed_coupon is not None:
            self.perform_actions(USE_COUPON)
            coupon_amount = 1

            self.perform_actions("swipe_accId_//", NON_SUPER_COMPOSED_COUPON_SWIPE_STOP, 'U',
                                 COUPON,
                                 COUPON_CONFIRM)
            actual_pay_amount = (decimal.Decimal(repay_amount) - decimal.Decimal(coupon_amount)).quantize(
                decimal.Decimal('0.00'))
            self.assert_values(str(actual_pay_amount),
                               self.get_text("//UIAStaticText[@label='应付金额']/following-sibling::UIAStaticText"), '==')

        self.perform_actions(
            REPAY_CONFIRM,
            TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_ios_xjb_3_0.credit_card_add_finish_page.CreditCardAddFinishPage(self.web_driver)
        return page

    # 转到预约还款页面
    @robot_log
    def go_to_reserved_pay_page(self):
        self.perform_actions(CREDIT_CARD_SELECTED)

        if self.element_exist("(UIButton_取消预约)", "find_element_by_accessibility_id"):
            self.perform_actions(CANCEL_RESERVATION,
                                 CANCEL_RESERVATION_CONFIRM)
        self.perform_actions(
                             RESERVATION_PAY,
                             )

        page = ReservedPayPage(self.web_driver)
        return page

    # 取消预约还款
    @robot_log
    def cancel_reservation(self):
        self.perform_actions(CREDIT_CARD_SELECTED,
                             CANCEL_RESERVATION
                             )

        self.perform_actions(CANCEL_RESERVATION_CONFIRM)

        self.assert_values("信用卡还款", self.get_text("//UIAStaticText[@label='信用卡还款']"))
        self.assert_values(False, self.element_exist("(UIButton_取消预约)", "find_element_by_accessibility_id"))

        page = self

        return page

    # 添加信用卡还款提醒
    @robot_log
    def add_repayment_warn(self):
        self.perform_actions(CREDIT_CARD_SELECTED,
                             CREDIT_CARD_SELECTED_DETAIL,
                             # REPAYMENT_WARN_SET,
                             REPAYMENT_WARN_SWITCH,
                             # REPAYMENT_WARN_DATE,
                             REPAYMENT_WARN_DATE_CONFIRM
                             )

        self.assert_values(True, self.element_is_displayed("(提醒日)", "find_element_by_accessibility_id"))

    # 取消信用卡还款提醒
    @robot_log
    def cancel_repayment_warn(self):
        time.sleep(0.5)
        self.perform_actions(CREDIT_CARD_SELECTED,
                             CREDIT_CARD_SELECTED_DETAIL,
                             # REPAYMENT_WARN_SET,
                             REPAYMENT_WARN_SWITCH,
                             # REPAYMENT_WARN_DATE,
                             REPAYMENT_WARN_DATE_CANCEL,
                             )

        self.assert_values(False, self.element_is_displayed("(提醒日)", "find_element_by_accessibility_id"))

    # 验证预约还款出现在相应的信用卡里
    @robot_log
    def verify_reserve_pay_info(self, last_card_no, amount):
        amount = decimal.Decimal(amount).quantize(decimal.Decimal('0.00'))

        self.assert_values("预约还款 %s" % amount, self.get_text(
            "//UIAStaticText[contains(@name, '**** **** **** %s')]/following-sibling::UIAStaticText[1]" % last_card_no))

    # 用户未绑定任何的储蓄卡，点击还信用卡时，提示需要先绑定一张储蓄卡，点击确定进入绑储蓄卡页面。(实名了则进入绑卡页面，未实名进入设置交易密码页面)
    @robot_log
    def go_to_bind_bank_card_page(self):
        self.assert_values("您需先绑定一张储蓄卡", self.get_text("(您需先绑定一张储蓄卡)", "find_element_by_accessibility_id"))
        self.perform_actions(TIPS_CONFIRM)

        page = huaxin_ui.ui_ios_xjb_3_0.binding_card_page.BindingCardPage(self.web_driver)
        return page
