# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import time
import huaxin_ui.ui_android_xjb_3_0.make_financing_plan_page

CHOOSE_BANKCARD = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tv_choose_bankcard_arrow']"
BANK_CARD = "xpath_//android.widget.TextView[contains(@text,'%s')]"
INPUT_MONEY = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cket_salary_fin_crud_money']"
TRANSFER_DATE = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_salary_fin_transfer_date']"
TRANSFER_DAY = "xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/day']"
TRANSFER_DATE_COMPELETED = "xpath_//android.widget.TextView[@text='完成']"
ADD_FINANCING_PLAN_COMFIRM = "xpath_//android.widget.Button[@text='确认']"
STOP_FINANCING_PLAN_COMFIRM = "xpath_//android.widget.Button[@text='确认']"

SWIPE_BEGAIN = "swipe_xpath_//"
DAY_SWIPE_STOP = "swipe_xpath_//scroll_8"

PAUSE_SALARY_FINANCING_PLAN = "xpath_//android.widget.TextView[contains(@text,'暂停')]"
# RESTART_SALARY_FINANCING_PLAN="xpath_//android.widget.TextView[contains(@text,'启用']"
RESTART_SALARY_FINANCING_PLAN = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_salary_financial_detail_action_start']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
MODIFY_SALARY_FINANCING_PLAN = "xpath_//android.widget.TextView[contains(@text,'修改')]"
STOP_SALARY_FINANCING_PLAN = "xpath_//android.widget.TextView[contains(@text,'终止')]"


class SalaryFinancingPlanDetailPage(PageObject):
    def __init__(self, web_driver):
        super(SalaryFinancingPlanDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('理财计划详情', self.get_text('//android.widget.TextView'))

        page = self
        return page

    @robot_log
    def pause_salary_financing_plan(self, trade_password):
        self.perform_actions(PAUSE_SALARY_FINANCING_PLAN,
                             TRADE_PASSWORD, trade_password)

        self.assert_values('已暂停', str(
            self.get_text('com.shhxzq.xjb:id/tv_salary_fin_detail_statusinfo', 'find_element_by_id')))

        page = self

        return page

    @robot_log
    def restart_salary_financing_plan(self, trade_password):
        self.assert_values('已暂停', self.get_text('com.shhxzq.xjb:id/tv_salary_fin_detail_statusinfo', 'find_element_by_id'))

        time.sleep(5)

        self.perform_actions(RESTART_SALARY_FINANCING_PLAN,
                             TRADE_PASSWORD, trade_password)

        page = self
        return page

    @robot_log
    def stop_salary_financing_plan(self, trade_password):
        time.sleep(5)

        self.perform_actions(STOP_SALARY_FINANCING_PLAN,
                             STOP_FINANCING_PLAN_COMFIRM,
                             TRADE_PASSWORD, trade_password)

        page = self
        self.assert_values('已终止', self.get_text('com.shhxzq.xjb:id/tv_salary_fin_detail_statusinfo', 'find_element_by_id'))

        return page

    @robot_log
    def go_to_modify_financing_plan_page(self):
        self.perform_actions(MODIFY_SALARY_FINANCING_PLAN)

        page = huaxin_ui.ui_android_xjb_3_0.make_financing_plan_page.MakeFinancingPlanPage(self.web_driver)

        time.sleep(5)
        return page
