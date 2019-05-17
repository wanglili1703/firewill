# coding: utf-8

from _common.page_object import PageObject
from _tools.mysql_xjb_tools import MysqlXjbTools
from _common.global_config import ASSERT_DICT
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.make_financing_plan_page
import huaxin_ui.ui_android_xjb_3_0.salary_financing_plan_detail_page
import time

SALARY_FINANCING_STATUS = "xpath_//android.widget.TextView[@text='未激活']"
START_SALARY_ISSUING = "xpath_//android.widget.ImageView[@NAF='true' and @instance='0']"
BINDING_PAY_CARD_MESSAGE_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
PHONE_NUMBER = "android.widget.EditText[@resource_id='com.shhxzq.xjb:id/bind_card_phonenumber']"
GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
VERIFY_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入验证码']"
NEXT = "xpath_//android.widget.Button[@text='下一步']"
SALARY_ISSUING_DONE = "xpath_//android.widget.Button[@text='确认']"
ADD_PLAN = "xpath_//android.widget.Button[@text='新增计划']"
START_SALARY_FINANCING = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/salary_fin_start_btn']"
SALARY_FINANCING_TITLE = "xpath_//android.widget.TextView[@text='UI自动化管理员员工理财']"
STOP_SALARY_ISSUING = "xpath_//android.widget.TextView[@text='终止']"
STOP_SALARY_ISSUING_COMFIRM = "xpath_//android.widget.Button[@text='确定']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
SALARY_FINANCING_PLAN = "xpath_//android.widget.TextView[contains(@text,'工资理财')]"

current_page = []


class DepositSalaryPage(PageObject):
    def __init__(self, web_driver):
        super(DepositSalaryPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('存工资',self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def start_salary_issuing(self):
        if self.element_exist("//android.widget.TextView[@text='未激活']"):
            self.perform_actions(SALARY_FINANCING_STATUS)

            self.perform_actions(START_SALARY_ISSUING)

            # self.perform_actions(BINDING_PAY_CARD_MESSAGE_CONFIRM,
            #                       PHONE_NUMBER,user_name,
            #                       GET_VERIFY_CODE)
            #
            # verification_code = MysqlXjbTools().get_sms_verify_code(mobile=user_name, template_id='cif_bindBankCard')
            #
            # self.perform_actions(VERIFY_CODE_INPUT, verification_code,
            #                       NEXT)

            self.perform_actions(SALARY_ISSUING_DONE)

            page = self

            time.sleep(3)
            self.assert_values('存工资', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))
            self.assert_values('已激活', self.get_text('com.shhxzq.xjb:id/tv_salary_fin_status', 'find_element_by_id'))
            return page

    @robot_log
    def go_to_make_financing_plan_page(self):
        if self.element_exist("//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/salary_fin_start_btn']"):
            self.perform_actions(START_SALARY_FINANCING)
        else:
            self.perform_actions(ADD_PLAN)

        page = huaxin_ui.ui_android_xjb_3_0.make_financing_plan_page.MakeFinancingPlanPage(self.web_driver)
        time.sleep(5)
        return page

    @robot_log
    def stop_salary_issuing(self, trade_password):
        self.perform_actions(SALARY_FINANCING_TITLE)

        self.assert_values('正常执行中',
                           self.get_text('com.shhxzq.xjb:id/tv_salary_fin_detail_statusinfo', 'find_element_by_id'))

        self.perform_actions(STOP_SALARY_ISSUING,
                             STOP_SALARY_ISSUING_COMFIRM,
                             TRADE_PASSWORD, trade_password)

        self.assert_values('已终止',
                           self.get_text('com.shhxzq.xjb:id/tv_salary_fin_detail_statusinfo', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_salary_financing_plan_detail_page(self):
        self.perform_actions(SALARY_FINANCING_PLAN)

        page = huaxin_ui.ui_android_xjb_3_0.salary_financing_plan_detail_page.SalaryFinancingPlanDetailPage(
            self.web_driver)

        return page
