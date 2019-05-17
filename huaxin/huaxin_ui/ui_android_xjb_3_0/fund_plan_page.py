# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_android_xjb_3_0.fund_plan_detail_page
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page
from _common.global_config import ASSERT_DICT
import time

AMOUNT="xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/product_purchase_amt']"
PURCHASE_CYCLE_WEEK_LIST="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_purchase_cycle_weak']"
PURCHASE_CYCLE_WEEK="xpath_//android.widget.ListView/android.widget.CheckedTextView[2]"
PURCHASE_CYCLE_WEEK_MODIFY="xpath_//android.widget.ListView/android.widget.CheckedTextView[3]"
PURCHASE_CYCLE_DAY_LIST="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_purchase_cycle_day']"
PURCHASE_CYCLE_DAY="xpath_//android.widget.ListView/android.widget.CheckedTextView[2]"
PURCHASE_CYCLE_DAY_MODIFY="xpath_//android.widget.ListView/android.widget.CheckedTextView[3]"
PURCHASE_COMFIRM="xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
PURCHASE_DONE = "xpath_//android.widget.Button[@text='确认']"
START_FUND_PLAN="xpath_//android.widget.Image[@resource-id='cunru']"
SWIPE_BEGIN="swipe_xpath_//"
COMFIRM_SWIPE_STOP="swipe_xpath_//android.widget.Button[@text='确认']"



current_page = []

class FundPlanPage(PageObject):
    def __init__(self, web_driver):
        super(FundPlanPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        # self.assert_values('我的定投计划', self.get_text('com.shhxzq.xjb:id/title_actionbar_orange', 'find_element_by_id'))
        self.assert_values('制定定投计划', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def make_fund_plan(self,amount,trade_password,return_page=None):

        time.sleep(15)

        if return_page is None:
            if self.element_exist("//android.widget.Image[@resource-id='cunru']", "find_element_by_xpath", 20):
                self.perform_actions(START_FUND_PLAN)

            self.perform_actions(AMOUNT,amount,
                                 PURCHASE_CYCLE_WEEK_LIST,
                                 PURCHASE_CYCLE_WEEK,
                                 PURCHASE_CYCLE_DAY_LIST,
                                 PURCHASE_CYCLE_DAY)
        else:
            self.perform_actions(AMOUNT, amount,
                                 PURCHASE_CYCLE_WEEK_LIST,
                                 PURCHASE_CYCLE_WEEK_MODIFY,
                                 PURCHASE_CYCLE_DAY_LIST,
                                 PURCHASE_CYCLE_DAY_MODIFY)

        purchase_cycle_week=self.get_text('com.shhxzq.xjb:id/tv_purchase_cycle_weak', 'find_element_by_id')
        purchase_cycle_day=self.get_text('com.shhxzq.xjb:id/tv_purchase_cycle_day', 'find_element_by_id')

        ASSERT_DICT.update({'purchase_cycle_week': purchase_cycle_week,
                            'purchase_cycle_day': purchase_cycle_day})

        self.perform_actions(SWIPE_BEGIN,COMFIRM_SWIPE_STOP,'U')

        self.perform_actions(PURCHASE_COMFIRM,
                             TRADE_PASSWORD,trade_password)

        page= huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)

        return page
