# coding: utf-8
from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import time
import huaxin_ui.ui_ios_xjb_3_0.repay_loan_page
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page
import huaxin_ui.ui_ios_xjb_3_0.repay_loan_plan_detail_page

CHOOSE_BANK_CARD = "xpathIOS_UIAStaticText_//UIAStaticText[@label='还至银行卡:']"
SWIPE_BEGIN = "swipe_accId_//"
SWIPE_DATE_END = "swipe_xpathIOS_//UIAPickerWheel[@value='1日']"

BANK_CARD_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[contains(@text,'1360')]"
REPAY_COUNT_SWIPE_STOP = "swipe_xpath_//android.widget.Button[@text='确认']"
BANK_CARD = "xpathIOS_UIAStaticText_//UIAStaticText[contains(@label, '%s')]"
DATE = "//UIAStaticText[@label='还款日期']/following-sibling::UIAStaticText"
NUMBER = "//UIAStaticText[@label='期数']/following-sibling::UIAStaticText"
REPAY_AMOUNT = "xpathIOS_UIATextField_IOS//UIAStaticText[@label='还款金额']/following-sibling::UIATextField"
REPAY_DATE = "xpathIOS_UIAStaticText_%s" % DATE
REPAY_DATA_SCROLL = "swipe_accId_scroll_5"
REPAY_DATE_COMPLETE = "accId_UIAButton_(UIButton_完成)"
REPAY_COUNT = "xpathIOS_UIAStaticText_%s" % NUMBER
REPAY_COUNT_SCROLL = "swipe_accId_scroll_5"
REPAY_COUNT_COMPLETE = "accId_UIAButton_完成"
REPAY_HOUSING_LOAN_CONFIRM = "accId_UIAButton_(UIButton_确定)"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
REPAY_HOUSING_LOAN_DONE = "accId_UIAButton_(UIButton_确认)"
REPAY_CAR_LOAN = "accId_UIAStaticText_还车贷"
REPAY_OTHERS = "accId_UIAStaticText_还其他"
REPAY_HOUSING_LOAN = "accId_UIAStaticText_还房贷"
HIDE_KEYBOARD = "accId_UIAButton_(UIButton_SafeKeyBoard_Hide)"
OTHER_PURPOSE = "xpathIOS_UIATextField_IOS//UIAStaticText[@label='还款用途']/following-sibling::UIATextField"


class MakeRepayPlanPage(PageObject):
    def __init__(self, web_driver):
        super(MakeRepayPlanPage, self).__init__(web_driver)

    @robot_log
    def verify_at_make_repay_loan_plan(self):
        self.assert_values('制定还款计划', self.get_text('//UIAStaticText[@name=\'制定还款计划\']'))

        page = self
        return page

    @robot_log
    def make_repay_loan_plan(self, trade_password, last_no, repay_amount, repay_type, other_purpose=None):

        if repay_type == 'car_loan':
            self.perform_actions(REPAY_CAR_LOAN)
        elif repay_type == 'others':
            self.perform_actions(REPAY_OTHERS)
            self.perform_actions(
                # this is just for work-around, no response after type words,
                # first, click word in the keyboard, then input words makes effect.
                OTHER_PURPOSE, other_purpose)

            self.perform_actions(
                "accId_UIAKey_t",
                "accId_UIAButton_Return",
                OTHER_PURPOSE, other_purpose)

        self.perform_actions(CHOOSE_BANK_CARD,
                             BANK_CARD % last_no,
                             REPAY_AMOUNT, repay_amount,
                             HIDE_KEYBOARD,
                             REPAY_DATE,
                             SWIPE_BEGIN, REPAY_DATA_SCROLL, 'U',
                             REPAY_DATE_COMPLETE,
                             REPAY_COUNT,
                             SWIPE_BEGIN, REPAY_COUNT_SCROLL, 'U',
                             REPAY_COUNT_COMPLETE)

        date = self.get_text(DATE)
        count = self.get_text(NUMBER)

        ASSERT_DICT.update({
            "repay_date": date,
            "repay_count": count
        })

        self.perform_actions(
            REPAY_HOUSING_LOAN_CONFIRM,
            TRADE_PASSWORD, trade_password,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)
        return page

    @robot_log
    def modify_repay_loan_plan(self, trade_password, last_no, repay_amount, repay_type, other_purpose=None):

        if repay_type == 'car_loan':
            self.perform_actions(REPAY_CAR_LOAN)
        elif repay_type == 'others':
            self.perform_actions(REPAY_OTHERS)
            self.perform_actions(
                # this is just for work-around, no response after type words,
                # first, click word in the keyboard, then inputing words makes effect.
                OTHER_PURPOSE, other_purpose,
                "accId_UIAKey_t",
                "accId_UIAButton_Return",
                OTHER_PURPOSE, other_purpose)
        else:
            self.perform_actions(REPAY_HOUSING_LOAN)

        self.perform_actions(CHOOSE_BANK_CARD,
                             BANK_CARD % last_no,
                             REPAY_AMOUNT, repay_amount,
                             HIDE_KEYBOARD,
                             REPAY_DATE,
                             SWIPE_BEGIN, REPAY_DATA_SCROLL, 'U',
                             REPAY_DATE_COMPLETE,
                             REPAY_COUNT,
                             SWIPE_BEGIN, REPAY_COUNT_SCROLL, 'U',
                             REPAY_COUNT_COMPLETE)

        date = self.get_text(DATE)
        count = self.get_text(NUMBER)
        ASSERT_DICT.update({
            "repay_date": date,
            "repay_count": count
        })
        self.perform_actions(
            REPAY_HOUSING_LOAN_CONFIRM,
            TRADE_PASSWORD, trade_password,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)
        return page
