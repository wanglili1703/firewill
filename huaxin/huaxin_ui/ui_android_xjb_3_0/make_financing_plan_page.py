# coding=utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.main_page
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_android_xjb_3_0.deposit_salary_page
import huaxin_ui.ui_android_xjb_3_0.salary_financing_plan_detail_page

CHOOSE_BANKCARD = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tv_choose_bankcard_arrow']"
BANK_CARD = "xpath_//android.widget.TextView[contains(@text,'%s')]"
INPUT_MONEY = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cket_salary_fin_crud_money']"
TRANSFER_DATE = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_salary_fin_transfer_date']"
TRANSFER_DAY = "xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/day']"
TRANSFER_AMOUNT = "xpath_//android.widget.TextView[@text='转入金额']"  # 为了收回安全键盘,后期可优化
TRANSFER_DATE_COMPELETED = "xpath_//android.widget.TextView[@text='完成']"
ADD_FINANCING_PLAN_COMFIRM = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
ADD_FINANCING_PLAN_DONE = "xpath_//android.widget.Button[@text='确认']"
MODIFY_FINANCING_PLAN_DONE = "xpath_//android.widget.Button[@text='确认']"

SWIPE_BEGAIN = "swipe_xpath_//"
DAY_SWIPE_STOP = "swipe_xpath_//scroll_8"

current_page = []


class MakeFinancingPlanPage(PageObject):
    def __init__(self, web_driver):
        super(MakeFinancingPlanPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('制定理财计划', self.get_text(self.page_title, 'find_element_by_id'))
        page = self
        return page

    @robot_log
    def make_financing_plan(self, last_no, amount, trade_password):
        self.perform_actions(CHOOSE_BANKCARD,
                             BANK_CARD % last_no,
                             INPUT_MONEY, amount,
                             TRANSFER_AMOUNT,
                             TRANSFER_DATE,
                             SWIPE_BEGAIN, DAY_SWIPE_STOP, 'U',
                             TRANSFER_DATE_COMPELETED,
                             ADD_FINANCING_PLAN_COMFIRM)

        self.assert_values('新增理财计划', self.get_text('com.shhxzq.xjb:id/trade_pop_info', 'find_element_by_id'))

        self.perform_actions(TRADE_PASSWORD, trade_password,
                             )

        self.assert_values('设置成功！', self.get_text('com.shhxzq.xjb:id/trade_succeed_info', 'find_element_by_id'))

        self.perform_actions(ADD_FINANCING_PLAN_DONE)

        page = huaxin_ui.ui_android_xjb_3_0.deposit_salary_page.DepositSalaryPage(self.web_driver)

        # ASSERT_DICT.update({'salary_financing_bankcard': self.perform_actions("getV_Android_com.shhxzq.xjb:id/dtv_salary_fin_bankcard[@text_]"),
        #                     'salary_financing_amount': self.perform_actions("getV_Android_com.shhxzq.xjb:id/dtv_salary_fin_everymonth_turn[@text_]"),
        #                     })

        return page

    @robot_log
    def modify_salary_financing_plan(self, trade_password, last_no, amount):
        self.perform_actions(CHOOSE_BANKCARD,
                             BANK_CARD % last_no,
                             INPUT_MONEY, amount,
                             TRANSFER_AMOUNT,
                             TRANSFER_DATE,
                             SWIPE_BEGAIN, DAY_SWIPE_STOP, 'U',
                             TRANSFER_DATE_COMPELETED,
                             ADD_FINANCING_PLAN_COMFIRM)

        self.assert_values('修改理财计划', self.get_text('com.shhxzq.xjb:id/trade_pop_info', 'find_element_by_id'))

        self.perform_actions(TRADE_PASSWORD, trade_password)

        self.assert_values('设置成功！', self.get_text('com.shhxzq.xjb:id/trade_succeed_info', 'find_element_by_id'))

        self.perform_actions(MODIFY_FINANCING_PLAN_DONE)

        page = huaxin_ui.ui_android_xjb_3_0.salary_financing_plan_detail_page.SalaryFinancingPlanDetailPage(
            self.web_driver)

        return page
