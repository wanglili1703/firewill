# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_plan_page
import huaxin_ui.ui_android_xjb_3_0.my_fund_plan_page
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_android_xjb_3_0.fund_history_plan_page

PAUSE = "xpath_//android.widget.TextView[@text='暂停']"
RESTART = "xpath_//android.widget.TextView[@text='恢复']"
STOP = "xpath_//android.widget.TextView[@text='终止']"
MODIFY = "xpath_//android.widget.TextView[@text='修改']"
CONFIRM = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
DELETE = "xpath_//android.widget.TextView[@text='删除']"
DELETE_CONFIRM = "xpath_//android.widget.Button[@text='确认']"


class FundPlanDetailPage(PageObject):
    def __init__(self, web_driver):
        super(FundPlanDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('定投详情', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_fund_plan_status(self, status):
        self.assert_values(status, self.get_text('com.shhxzq.xjb:id/tv_fund_plan_details_title', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def pause_fund_plan(self, trade_password):
        self.perform_actions(PAUSE,
                             CONFIRM,
                             TRADE_PASSWORD, trade_password)

        page = self

        return page

    @robot_log
    def restart_fund_plan(self, trade_password):
        self.perform_actions(RESTART,
                             CONFIRM,
                             TRADE_PASSWORD, trade_password)

        page = self

        return page

    @robot_log
    def stop_fund_plan(self, trade_password):
        self.perform_actions(STOP,
                             CONFIRM,
                             TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_android_xjb_3_0.my_fund_plan_page.MyFundPlanPage(self.web_driver)

        return page

    @robot_log
    def go_to_make_fund_plan_page(self):
        self.perform_actions(MODIFY)

        page = huaxin_ui.ui_android_xjb_3_0.fund_plan_page.FundPlanPage(self.web_driver)

        return page

    @robot_log
    def verify_fund_plan_details(self, amount):
        self.assert_values(amount, self.get_text(
            "//android.widget.TextView[@text='每期定投(元)']/../following-sibling::android.widget.LinearLayout[1]/android.widget.TextView[@resource-id='com.shhxzq.xjb:id/content']"))

        self.assert_values(ASSERT_DICT['purchase_cycle_week'], self.get_text(
            "//android.widget.TextView[@text='扣款周期']/../following-sibling::android.widget.LinearLayout[1]/android.widget.TextView[@resource-id='com.shhxzq.xjb:id/content']"))
        self.assert_values(ASSERT_DICT['purchase_cycle_day'], self.get_text(
            "//android.widget.TextView[@text='扣款日期']/../following-sibling::android.widget.LinearLayout[1]/android.widget.TextView[@resource-id='com.shhxzq.xjb:id/content']"))

        page = self

        return page

    @robot_log
    def get_fund_plan_details(self):
        amount = self.get_text(
            "//android.widget.TextView[@text='每期定投(元)']/../following-sibling::android.widget.LinearLayout[1]/android.widget.TextView[@resource-id='com.shhxzq.xjb:id/content']")
        ASSERT_DICT.update({'amount': amount})

        page = self

        return page

    @robot_log
    def delete_fund_history_plan(self):
        self.perform_actions(DELETE,
                             DELETE_CONFIRM)

        page = huaxin_ui.ui_android_xjb_3_0.fund_history_plan_page.FundHistoryPlanPage(self.web_driver)
        return page
