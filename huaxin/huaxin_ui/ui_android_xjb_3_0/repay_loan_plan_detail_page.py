# coding:utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.make_repay_plan_page
import huaxin_ui.ui_android_xjb_3_0.repay_loan_page
import time

PAUSE_BUTTON = "xpath_//android.widget.TextView[@text='暂停']"
RESTART_BUTTON = "xpath_//android.widget.TextView[@text='启用']"
MODIFY_BUTTON = "xpath_//android.widget.TextView[@text='修改']"
DELETE_BUTTON = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/ibtn_actionbar_right']"
DELETE = "xpath_//android.widget.TextView[@text='删除']"
MODIFY_BUTTON_OTHER_LOAN = "xpath_//android.widget.TextView[@text='修改']"
COMFIRM = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"


class RepayLoanPlanDetailPage(PageObject):
    def __init__(self, web_driver):
        super(RepayLoanPlanDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('还贷款详情', self.get_text('com.shhxzq.xjb:id/title_actionbar','find_element_by_id'))

        page = self
        return page

    @robot_log
    def pause_repay_loan_plan(self, trade_password):
        self.perform_actions(PAUSE_BUTTON,
                             COMFIRM,
                             TRADE_PASSWORD,trade_password)

        time.sleep(3)
        self.assert_values('已暂停', self.get_text('com.shhxzq.xjb:id/tv_repay_loan_detail_statusinfo','find_element_by_id'))

        page = self

        return page

    @robot_log
    def restart_repay_loan_plan(self, trade_password):
        self.perform_actions(RESTART_BUTTON,
                             COMFIRM,
                             TRADE_PASSWORD, trade_password)

        self.assert_values('暂停', self.get_text('com.shhxzq.xjb:id/tv_loan_repay_detail_action_start','find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_modify_repay_loan_plan_page(self):
        self.perform_actions(MODIFY_BUTTON)

        page = huaxin_ui.ui_android_xjb_3_0.make_repay_plan_page.MakeRepayPlanPage(self.web_driver)

        time.sleep(3)

        self.assert_values('制定还款计划', self.get_text('com.shhxzq.xjb:id/title_actionbar','find_element_by_id'))

        return page

    @robot_log
    def delete_repay_loan_plan(self, trade_password):
        self.perform_actions(DELETE_BUTTON,
                             DELETE,
                             COMFIRM)

        self.perform_actions(TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_android_xjb_3_0.repay_loan_page.RepayLoanPage(self.web_driver)

        time.sleep(3)

        self.assert_values('还贷款', self.get_text('com.shhxzq.xjb:id/title_actionbar','find_element_by_id'))

        return page
