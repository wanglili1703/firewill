# coding=utf-8
import time

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.assets_page
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page

REGULAR_WITHDRAW_RADIO = "accId_UIAStaticText_普通取出"
FAST_WITHDRAW_RADIO = "accId_UIAStaticText_快速取出"
AMOUNT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATableView/UIATableCell[4]/UIATextField"
CONFIRM_BUTTON = "accId_UIAButton_确认取出"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"

current_page = []


class WithdrawPage(PageObject):
    def __init__(self, web_driver):
        super(WithdrawPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
            'AssetsPage': huaxin_ui.ui_ios_xjb_3_0.assets_page.AssetsPage(self.web_driver)
        }

    @robot_log
    def verify_at_withdraw_page(self):
        self.assert_values(True, self.element_exist("取出", "find_element_by_accessibility_id"))

    @robot_log
    def fast_withdraw(self, withdraw_amount, trade_password, return_page=None):
        self.perform_actions(
            FAST_WITHDRAW_RADIO,
            AMOUNT, withdraw_amount,
            CONFIRM_BUTTON
        )

        if (float(withdraw_amount)) > 0 and (float(withdraw_amount) < 999999999):
            self.perform_actions(
                TRADE_PASSWORD, trade_password,
            )

            time.sleep(1.5)
            page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)
        else:
            page = self
        return page

    @robot_log
    def regular_withdraw(self, withdraw_amount, trade_password, return_page=None):
        self.perform_actions(
            REGULAR_WITHDRAW_RADIO,
            AMOUNT, withdraw_amount,
            CONFIRM_BUTTON,
        )

        if (float(withdraw_amount)) > 0 and (float(withdraw_amount) < 999999999):
            self.perform_actions(
                TRADE_PASSWORD, trade_password,
            )

            time.sleep(1.5)
            page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)
        else:
            page = self

        return page
