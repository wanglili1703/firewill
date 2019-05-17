# coding: utf-8
import huaxin_ui
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.calendar_page
import huaxin_ui.ui_ios_xjb_3_0.credit_card_repay_page
import huaxin_ui.ui_ios_xjb_3_0.salary_financing_plan_detail_page
import huaxin_ui.ui_ios_xjb_3_0.deposit_salary_page
import huaxin_ui.ui_ios_xjb_3_0.repay_loan_page
import huaxin_ui.ui_ios_xjb_3_0.fund_page_all_fund_page

LEFT_BUTTON = "accId_UIAButton_UIBarButtonItemLocationLeft"
CREDIT_REPAY_SETTING = "accId_UIAButton_信用卡还款"
SALARY_SETTING = "accId_UIAButton_工资理财"
LOAN_SETTING = "accId_UIAButton_还贷款"
FUND_INVEST_SETTING = "accId_UIAButton_基金定投"
current_page = []


class PersonalEventSettingPage(PageObject):
    def __init__(self, web_driver):
        super(PersonalEventSettingPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_back_to_calendar_page(self):
        self.perform_actions(LEFT_BUTTON)

        page = huaxin_ui.ui_ios_xjb_3_0.calendar_page.CalendarPage(self.web_driver)
        return page

    @robot_log
    def verify_at_personal_event_setting_page(self):
        self.assert_values("个人事项设置", self.get_text("//UIAStaticText[@label='个人事项设置']"))

        page = self
        return page

    @robot_log
    def go_to_credit_card_list_page(self):
        self.perform_actions(CREDIT_REPAY_SETTING)

        page = huaxin_ui.ui_ios_xjb_3_0.credit_card_repay_page.CreditCardRepayPage(self.web_driver)
        return page

    @robot_log
    def go_to_salary_financing_page(self):
        self.perform_actions(SALARY_SETTING)

        page = huaxin_ui.ui_ios_xjb_3_0.salary_financing_plan_detail_page.SalaryFinancingPlanDetailPage(self.web_driver)
        return page

    @robot_log
    def go_to_loan_page(self):
        self.perform_actions(LOAN_SETTING)

        page = huaxin_ui.ui_ios_xjb_3_0.repay_loan_page.RepayLoanPage(self.web_driver)
        return page

    @robot_log
    def go_to_all_fund_page(self):
        self.perform_actions(FUND_INVEST_SETTING)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_page_all_fund_page.FundPageAllFundPage(self.web_driver)
        return page
