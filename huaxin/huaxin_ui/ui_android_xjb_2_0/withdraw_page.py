# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_2_0.home_page
import huaxin_ui.ui_android_xjb_2_0.assets_page
import huaxin_ui.ui_android_xjb_2_0.home_page

REGULAR_WITHDRAW_RADIO = "xpath_//android.widget.RadioButton[@resource-id='com.shhxzq.xjb:id/rbtn_enchashment_normal_select']"
FAST_WITHDRAW_RADIO = "xpath_//android.widget.RadioButton[@resource-id='com.shhxzq.xjb:id/rbtn_enchashment_faster_select']"
AMOUNT = "xpath_//android.widget.EditText[@text='请输入取出金额']"
CONFIRM_BUTTON = "xpath_//android.widget.Button[@text='确认取出']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
SUCCESS_BUTTON = "xpath_//android.widget.Button[@text='确认']"

current_page = []


class WithdrawPage(PageObject):
    def __init__(self, web_driver):
        super(WithdrawPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
            'AssetsPage': huaxin_ui.ui_android_xjb_2_0.assets_page.AssetsPage(self.web_driver)
        }

    @robot_log
    def fast_withdraw(self, withdraw_amount, trade_password, return_page=None):
        self.perform_actions(
            FAST_WITHDRAW_RADIO,
            AMOUNT, withdraw_amount,
            CONFIRM_BUTTON,
            TRADE_PASSWORD, trade_password,
            SUCCESS_BUTTON
        )

        page = huaxin_ui.ui_android_xjb_2_0.home_page.HomePage(self.web_driver) if return_page is None else self._return_page[return_page]
        return page

    @robot_log
    def regular_withdraw(self, withdraw_amount, trade_password, return_page=None):
        self.perform_actions(
            REGULAR_WITHDRAW_RADIO,
            AMOUNT, withdraw_amount,
            CONFIRM_BUTTON,
            TRADE_PASSWORD, trade_password,
            SUCCESS_BUTTON
        )

        page = huaxin_ui.ui_android_xjb_2_0.home_page.HomePage(self.web_driver) if return_page is None else self._return_page[return_page]

        return page
