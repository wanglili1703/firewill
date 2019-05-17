# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_2_0.home_page
import huaxin_ui.ui_android_xjb_2_0.assets_xjb_detail_page

RECHARGE_AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cedt_recharge_amount']"
RECHARGE_CONFIRM_BUTTON = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
SUCCESS_BUTTON = "xpath_//android.widget.Button[@text='确认']"

current_page = []


class RechargePage(PageObject):
    def __init__(self, web_driver):
        super(RechargePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

        self._return_page = {
            'AssetsXjbDetailPage': huaxin_ui.ui_android_xjb_2_0.assets_xjb_detail_page.AssetsXjbDetailPage(
                self.web_driver)
        }

    @robot_log
    def recharge(self, recharge_amount, trade_password, return_page=None):
        self.perform_actions(
            RECHARGE_AMOUNT, recharge_amount,
            RECHARGE_CONFIRM_BUTTON,
            TRADE_PASSWORD, trade_password,
            SUCCESS_BUTTON,
        )

        page = huaxin_ui.ui_android_xjb_2_0.home_page.HomePage(self.web_driver) if return_page is None else self._return_page[return_page]
        return page
