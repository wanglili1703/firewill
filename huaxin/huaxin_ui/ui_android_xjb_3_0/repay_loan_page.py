# coding:utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.make_repay_plan_page
import huaxin_ui.ui_android_xjb_3_0.repay_loan_plan_detail_page
import time

MAKE_REPAY_PLAN = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/salary_fin_start_btn']"
ADD_REPAY_PLAN = "xpath_//android.widget.TextView[@text='新增还款计划']"
REPAY_HOUSING_LOAN = "xpath_//android.widget.TextView[@text='还房贷']"
REPAY_CAR_LOAN = "xpath_//android.widget.TextView[@text='还车贷']"
OTHER_LOAN = "xpath_//android.widget.TextView[@text='其他用途']"


class RepayLoanPage(PageObject):
    def __init__(self, web_driver):
        super(RepayLoanPage, self).__init__(web_driver)

    @robot_log
    def go_to_make_repay_plan_page(self):
        if self.element_exist("//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/salary_fin_start_btn']"):
            self.perform_actions(MAKE_REPAY_PLAN)
        else:
            self.perform_actions(ADD_REPAY_PLAN)

        page = huaxin_ui.ui_android_xjb_3_0.make_repay_plan_page.MakeRepayPlanPage(self.web_driver)

        time.sleep(5)

        return page

    @robot_log
    def go_to_repay_loan_plan_detail_page(self, repay_type=None):

        if repay_type == 'housing_loan':
            self.perform_actions(REPAY_HOUSING_LOAN)

        elif repay_type == 'car_loan':
            self.perform_actions(REPAY_CAR_LOAN)

        else:
            self.perform_actions(OTHER_LOAN)

        page = huaxin_ui.ui_android_xjb_3_0.repay_loan_plan_detail_page.RepayLoanPlanDetailPage(self.web_driver)

        time.sleep(3)

        return page
