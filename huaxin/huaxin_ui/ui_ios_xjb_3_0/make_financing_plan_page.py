# coding=utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.main_page
import huaxin_ui.ui_ios_xjb_3_0.deposit_salary_page
import huaxin_ui.ui_ios_xjb_3_0.salary_financing_plan_detail_page
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page

CHOOSE_BANKCARD = "accId_UIAStaticText_(支付方式:)"
BANK_CARD = "xpathIOS_UIAStaticText_//UIAStaticText[contains(@label, '%s')]"
INPUT_MONEY = "xpathIOS_UIATextField_IOS//UIATextField[@value='建议转入100元以上']"
MODIFY_MONEY = "xpathIOS_UIATextField_IOS//UIAStaticText[@label='¥']/following-sibling::UIATextField"
TRANSFER_DATE = "accId_UIAStaticText_转入日期"
HIDE_KEYBOARD = "accId_UIAButton_(UIButton_SafeKeyBoard_Hide)"
TRANSFER_DATE_COMPLETED = "accId_UIAButton_完成"
ADD_FINANCING_PLAN_CONFIRM = "accId_UIAButton_确定"
TRADE_PASSWORD = "xpathIOS_UIATextField_//UIAStaticText[@label='请输入交易密码']/following-sibling::UIATextField"
ADD_FINANCING_PLAN_DONE = "accId_UIAButton_确认"
MODIFY_FINANCING_PLAN_DONE = "accId_UIAButton_确认"

SWIPE_BEGAIN = "swipe_xpath_//"
DAY_SWIPE_STOP = "swipe_accId_scroll_8"

current_page = []


class MakeFinancingPlanPage(PageObject):
    def __init__(self, web_driver):
        super(MakeFinancingPlanPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_make_finance_plan_page(self):
        self.assert_values('制定理财计划', self.get_text("//UIAStaticText[@label='制定理财计划']"))

        page = self
        return page

    @robot_log
    def make_financing_plan(self, last_no, amount, trade_password):
        self.perform_actions(CHOOSE_BANKCARD,
                             BANK_CARD % last_no,
                             INPUT_MONEY, amount,
                             HIDE_KEYBOARD,
                             TRANSFER_DATE,
                             SWIPE_BEGAIN, DAY_SWIPE_STOP, 'U',
                             TRANSFER_DATE_COMPLETED,
                             ADD_FINANCING_PLAN_CONFIRM)

        self.perform_actions(TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page

    @robot_log
    def modify_salary_financing_plan(self, trade_password, last_no, amount):
        self.perform_actions(CHOOSE_BANKCARD,
                             BANK_CARD % last_no,
                             MODIFY_MONEY, amount,
                             HIDE_KEYBOARD,
                             TRANSFER_DATE,
                             SWIPE_BEGAIN, DAY_SWIPE_STOP, 'U',
                             TRANSFER_DATE_COMPLETED,
                             ADD_FINANCING_PLAN_CONFIRM)

        self.verify_at_make_finance_plan_page()
        self.perform_actions(TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)
        return page
