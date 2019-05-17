# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import time
import huaxin_ui.ui_ios_xjb_3_0.make_financing_plan_page

CHOOSE_BANKCARD = "accId_UIAStaticText_(支付方式:)"
BANK_CARD = "xpathIOS_UIAStaticText_//UIAStaticText[contains(@label, '%s')]"
INPUT_MONEY = "xpathIOS_UIATextField_IOS//UIATextField[@value='建议转入100元以上']"
TRANSFER_DATE = "accId_UIAStaticText_转入日期"
HIDE_KEYBOARD = "accId_UIAButton_(UIButton_SafeKeyBoard_Hide)"
TRANSFER_DATE_COMPLETED = "accId_UIAButton_完成"
STOP_FINANCING_PLAN_CONFIRM = "accId_UIAButton_确认"

PAUSE_SALARY_FINANCING_PLAN = "accId_UIAButton_暂停"
RESTART_SALARY_FINANCING_PLAN = "accId_UIAButton_启用"
TRADE_PASSWORD = "xpathIOS_UIATextField_//UIAStaticText[@label='请输入交易密码']/following-sibling::UIATextField"
MODIFY_SALARY_FINANCING_PLAN = "accId_UIAButton_修改"
STOP_SALARY_FINANCING_PLAN = "accId_UIAButton_终止"


class SalaryFinancingPlanDetailPage(PageObject):
    def __init__(self, web_driver):
        super(SalaryFinancingPlanDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_at_salary_detail_title(self):
        self.assert_values('理财计划详情', self.get_text("//UIAStaticText[@label='理财计划详情']"))

        page = self
        return page

    @robot_log
    def pause_salary_financing_plan(self, trade_password):
        self.assert_values('正常执行中', self.get_text('正常执行中', 'find_element_by_accessibility_id'))

        self.perform_actions(PAUSE_SALARY_FINANCING_PLAN,
                             STOP_FINANCING_PLAN_CONFIRM,
                             TRADE_PASSWORD, trade_password)

        self.assert_values('已暂停', self.get_text('已暂停', 'find_element_by_accessibility_id'))

        page = self

        return page

    @robot_log
    def restart_salary_financing_plan(self, trade_password):
        self.assert_values('已暂停', self.get_text('已暂停', 'find_element_by_accessibility_id'))

        self.perform_actions(RESTART_SALARY_FINANCING_PLAN,
                             STOP_FINANCING_PLAN_CONFIRM,
                             TRADE_PASSWORD, trade_password)

        self.assert_values('正常执行中', self.get_text('正常执行中', 'find_element_by_accessibility_id'))
        page = self
        return page

    @robot_log
    def stop_salary_financing_plan(self, trade_password):
        self.perform_actions(STOP_SALARY_FINANCING_PLAN,
                             STOP_FINANCING_PLAN_CONFIRM,
                             TRADE_PASSWORD, trade_password)

        self.assert_values('已终止', self.get_text('已终止', 'find_element_by_accessibility_id'))
        page = self

        return page

    @robot_log
    def go_to_modify_financing_plan_page(self):
        self.perform_actions(MODIFY_SALARY_FINANCING_PLAN)

        page = huaxin_ui.ui_ios_xjb_3_0.make_financing_plan_page.MakeFinancingPlanPage(self.web_driver)

        return page
