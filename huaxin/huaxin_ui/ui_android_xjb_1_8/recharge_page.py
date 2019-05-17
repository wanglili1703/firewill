from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_1_8.home_page import HomePage

RECHARGE_AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cedt_recharge_amount']"
RECHARGE_CONFIRM_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_recharge_next']"
SUCCESS_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/useroperation_succeed_bt']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"

current_page = []


class RechargePage(PageObject):
    def __init__(self, web_driver):
        super(RechargePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def recharge(self, recharge_amount, trade_password):
        self.perform_actions(
            RECHARGE_AMOUNT, recharge_amount,
            RECHARGE_CONFIRM_BUTTON,
        )

        self.perform_actions(
            TRADE_PASSWORD, trade_password,
            SUCCESS_BUTTON,
        )

        page = HomePage(self.web_driver)
        return page
