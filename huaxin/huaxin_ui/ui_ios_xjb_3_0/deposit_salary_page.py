# coding: utf-8

from _common.page_object import PageObject
from _tools.mysql_xjb_tools import MysqlXjbTools
from _common.global_config import ASSERT_DICT
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.make_financing_plan_page
import huaxin_ui.ui_ios_xjb_3_0.salary_financing_plan_detail_page
import time

SALARY_FINANCING_STATUS = "accId_UIAButton_未激活"
START_SALARY_ISSUING = "accId_UIAButton_(UIButton_开通员工理财)"
BINDING_PAY_CARD_MESSAGE_CONFIRM = "accId_UIAButton_确认"
PHONE_NUMBER = "accId_UIAButton_请输入手机号码"
GET_VERIFY_CODE = "accId_UIAButton_获取验证码"
VERIFY_CODE_INPUT = "accId_UIATextField_请输入验证码"
NEXT = "accId_UIAButton_下一步"
SALARY_ISSUING_DONE = "accId_UIAButton_(UIButton_确认)"
ADD_PLAN = "accId_UIAButton_新增计划"
START_SALARY_PLAN = "(UIButton_开启我的工资理财)"
START_SALARY_FINANCING = "accId_UIAButton_%s" % START_SALARY_PLAN
SALARY_FINANCING_TITLE = "accId_UIAStaticText_(yy_开户随心借f员工理财)"
STOP_SALARY_ISSUING = "xpathIOS_UIAButton_//UIAButton[@label='终止' and @visible='true']"
STOP_SALARY_ISSUING_CONFIRM = "accId_UIAButton_确认"
TRADE_PASSWORD = "xpathIOS_UIATextField_//UIATextField"
SALARY_FINANCING_PLAN = "accId_UIAButton_工资理财"

current_page = []


class DepositSalaryPage(PageObject):
    def __init__(self, web_driver):
        super(DepositSalaryPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('存工资', self.get_text('//UIAStaticText[@label=\'存工资\']'))

        page = self
        return page

    @robot_log
    def start_salary_issuing(self):
        if self.element_exist("未激活", "find_element_by_accessibility_id"):
            self.perform_actions(SALARY_FINANCING_STATUS)

            self.perform_actions(START_SALARY_ISSUING)

            self.perform_actions(SALARY_ISSUING_DONE)

            page = self

            time.sleep(1)
            self.verify_page_title()
            self.assert_values('已激活', self.get_text("已激活", "find_element_by_accessibility_id"))

            return page

    @robot_log
    def go_to_make_financing_plan_page(self):
        if self.element_exist(START_SALARY_PLAN, "find_element_by_accessibility_id"):
            self.perform_actions(START_SALARY_FINANCING)
        else:
            self.perform_actions(ADD_PLAN)

        page = huaxin_ui.ui_ios_xjb_3_0.make_financing_plan_page.MakeFinancingPlanPage(self.web_driver)

        page.verify_at_make_finance_plan_page()

        return page

    @robot_log
    def stop_salary_issuing(self, trade_password):
        self.perform_actions(SALARY_FINANCING_TITLE)

        self.assert_values('正常执行中',
                           self.get_text('(正常执行中)', 'find_element_by_accessibility_id'))

        self.perform_actions(STOP_SALARY_ISSUING,
                             STOP_SALARY_ISSUING_CONFIRM,
                             TRADE_PASSWORD, trade_password)

        self.assert_values('已终止',
                           self.get_text('已终止', 'find_element_by_accessibility_id'))

        page = huaxin_ui.ui_ios_xjb_3_0.salary_financing_plan_detail_page.SalaryFinancingPlanDetailPage(
            self.web_driver)

        return page

    @robot_log
    def go_to_salary_financing_plan_detail_page(self):
        self.perform_actions(SALARY_FINANCING_PLAN)

        page = huaxin_ui.ui_ios_xjb_3_0.salary_financing_plan_detail_page.SalaryFinancingPlanDetailPage(
            self.web_driver)

        return page
