# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.repay_loan_page
import huaxin_ui.ui_android_xjb_3_0.repay_loan_plan_detail_page
import time

CHOOSE_BANK_CARD = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tv_choose_bankcard_arrow']"
SWIPE_BEGIN = "swipe_xpath_//"
BANK_CARD_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[contains(@text,'%s')]"
REPAY_COUNT_SWIPE_STOP = "swipe_xpath_//android.widget.Button[@text='确认']"
BANK_CARD = "xpath_//android.widget.TextView[contains(@text,'%s')]"
REPAY_AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cket_loan_repay_crud_money']"
REPAY_DATE = "xpath_//android.widget.TextView[@text='还款日期']"
REPAY_DATA_SCROLL = "swipe_xpath_//scroll_8"
REPAY_DATE_COMPELETE = "xpath_//android.widget.TextView[@text='完成']"
REPAY_COUNT = "xpath_//android.widget.TextView[@text='期数']"
REPAY_COUNT_SCROLL = "swipe_xpath_//scroll_8"
REPAY_COUNT_COMPELETE = "xpath_//android.widget.TextView[@text='完成']"
REPAY_HOUSING_LOAN_COMFIRM = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
REPAY_HOUSING_LOAN_DONE = "xpath_//android.widget.Button[@text='确认']"
REPAY_CAR_LOAN = "xpath_//android.widget.RadioButton[@text='还车贷']"
REPAY_OTHERS = "xpath_//android.widget.RadioButton[@text='还其他']"
REPAY_HOUSING_LOAN = "xpath_//android.widget.RadioButton[@text='还房贷']"
OTHER_PURPOSE = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/et_loan_repay_crud_comment']"
BACK="xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"

class MakeRepayPlanPage(PageObject):
    def __init__(self, web_driver):
        super(MakeRepayPlanPage, self).__init__(web_driver)

    @robot_log
    def make_repay_loan_plan(self, trade_password, last_no, repay_amount, repay_type, other_purpose=None):

        if repay_type == 'car_loan':
            self.perform_actions(REPAY_CAR_LOAN)
        elif repay_type == 'others':
            self.perform_actions(REPAY_OTHERS)
            time.sleep(5)
            self.perform_actions(OTHER_PURPOSE, other_purpose)

        self.perform_actions(CHOOSE_BANK_CARD,
                             SWIPE_BEGIN, BANK_CARD_SWIPE_STOP % last_no, 'U',
                             BANK_CARD % last_no,
                             REPAY_AMOUNT, repay_amount,
                             REPAY_DATE,
                             SWIPE_BEGIN, REPAY_DATA_SCROLL, 'U',
                             REPAY_DATE_COMPELETE,
                             SWIPE_BEGIN, REPAY_COUNT_SWIPE_STOP, 'U',
                             REPAY_COUNT,
                             SWIPE_BEGIN, REPAY_COUNT_SCROLL, 'U',
                             REPAY_COUNT_COMPELETE,
                             REPAY_HOUSING_LOAN_COMFIRM,
                             TRADE_PASSWORD, trade_password,
                             )
        time.sleep(5)
        self.assert_values('设置成功', self.get_text('com.shhxzq.xjb:id/trade_succeed_info','find_element_by_id'))

        self.perform_actions(REPAY_HOUSING_LOAN_DONE)

        page = huaxin_ui.ui_android_xjb_3_0.repay_loan_page.RepayLoanPage(self.web_driver)

        if repay_type == 'housing_loan':
            self.assert_values('还房贷', self.get_text('com.shhxzq.xjb:id/item_tv_loan_repay_title','find_element_by_id'))
        elif repay_type == 'car_loan':
            self.assert_values('还车贷', self.get_text('com.shhxzq.xjb:id/item_tv_loan_repay_title','find_element_by_id'))
        else:
            self.assert_values(str(other_purpose), self.get_text('com.shhxzq.xjb:id/item_tv_loan_repay_title','find_element_by_id'))

        return page

    @robot_log
    def modify_repay_loan_plan(self, trade_password, last_no, repay_amount, repay_type, other_purpose=None):

        if repay_type == 'car_loan':
            self.perform_actions(REPAY_CAR_LOAN)
        elif repay_type == 'others':
            self.perform_actions(REPAY_OTHERS)
            time.sleep(5)
            self.perform_actions(OTHER_PURPOSE, other_purpose)
        else:
            self.perform_actions(REPAY_HOUSING_LOAN)

        self.perform_actions(CHOOSE_BANK_CARD,
                             SWIPE_BEGIN, BANK_CARD_SWIPE_STOP % last_no, 'U',
                             BANK_CARD % last_no,
                             REPAY_AMOUNT, repay_amount,
                             REPAY_DATE,
                             SWIPE_BEGIN, REPAY_DATA_SCROLL, 'U',
                             REPAY_DATE_COMPELETE,
                             SWIPE_BEGIN, REPAY_COUNT_SWIPE_STOP, 'U',
                             REPAY_COUNT,
                             SWIPE_BEGIN, REPAY_COUNT_SCROLL, 'U',
                             REPAY_COUNT_COMPELETE,
                             REPAY_HOUSING_LOAN_COMFIRM,
                             TRADE_PASSWORD, trade_password,
                             )
        time.sleep(5)

        self.assert_values('设置成功', self.get_text('com.shhxzq.xjb:id/trade_succeed_info','find_element_by_id'))

        self.perform_actions(REPAY_HOUSING_LOAN_DONE)

        page = huaxin_ui.ui_android_xjb_3_0.repay_loan_plan_detail_page.RepayLoanPlanDetailPage(self.web_driver)

        self.perform_actions(BACK)

        if repay_type == 'housing_loan':
            self.assert_values('还房贷', self.get_text('com.shhxzq.xjb:id/item_tv_loan_repay_title','find_element_by_id'))
        elif repay_type == 'car_loan':
            self.assert_values('还车贷', self.get_text('com.shhxzq.xjb:id/item_tv_loan_repay_title','find_element_by_id'))
        else:
            self.assert_values(str(other_purpose), self.get_text('com.shhxzq.xjb:id/item_tv_loan_repay_title','find_element_by_id'))

        return page
