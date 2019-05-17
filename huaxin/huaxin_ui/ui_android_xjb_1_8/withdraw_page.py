from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_1_8.home_page import HomePage

REGULAR_WITHDRAW_RADIO = "xpath_//android.widget.RadioButton[@resource-id='com.shhxzq.xjb:id/rbtn_enchashment_normal_select']"
FAST_WITHDRAW_RADIO = "xpath_//android.widget.RadioButton[@resource-id='com.shhxzq.xjb:id/rbtn_enchashment_faster_select']"
AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cedt_enchashment_amount']"
CONFIRM_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_enchashment_confirm']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
SUCCESS_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/useroperation_succeed_bt']"

current_page = []


class WithdrawPage(PageObject):
    def __init__(self, web_driver):
        super(WithdrawPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def fast_withdraw(self, withdraw_amount, trade_password):
        self.perform_actions(
            FAST_WITHDRAW_RADIO,
            AMOUNT, withdraw_amount,
            CONFIRM_BUTTON,
        )

        self.perform_actions(
            TRADE_PASSWORD, trade_password,
            SUCCESS_BUTTON
        )

        page = HomePage(self.web_driver)
        return page

    @robot_log
    def regular_withdraw(self, withdraw_amount, trade_password):
        self.perform_actions(
            REGULAR_WITHDRAW_RADIO,
            AMOUNT, withdraw_amount,
            CONFIRM_BUTTON,
        )

        self.perform_actions(
            TRADE_PASSWORD, trade_password,
            SUCCESS_BUTTON
        )

        page = HomePage(self.web_driver)
        return page
