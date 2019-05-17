# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_2_0.trade_detail_page import TradeDetailPage

TRADE_DETAIL = "accId_UIAButton_交易记录"
HIGH_END_MORE_PRODUCT = "accId_UIAButton_查看更多产品"

HIGH_END_START = "swipe_accId_高端"
HISTORY_PRODUCT_STOP = "swipe_accId_查看历史产品"
HISTORY_PRODUCT = "accId_UIAButton_查看历史产品"

TITLE_START = "swipe_accId_高端理财"
HIGH_END_PRODUCT_STOP = "swipe_accId_%s"
HIGH_END_PRODUCT = "accId_UIAStaticText_%s"
REDEEM = "accId_UIAButton_卖出"
REDEEM_AMOUNT = "accId_UIATextField_(redeemTextField)请输入卖出份额"
REDEEM_AMOUNT_2 = "accId_UIATextField_(textField)请输入卖出份额"
NORMAL_REDEEM_VIPPRODUCT_AMOUNT = "accId_UIATextField_(redeemTextField)请输入卖出份额"
REDEEM_CONFIRM = "accId_UIAButton_确认"
TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
REDEEM_DONE = "accId_UIAButton_确认"

NORMAL_REDEEM="accId_UIAButton_(ordinaryButton)"
FAST_REDEEM="accId_UIAButton_(speedButton)"

current_page = []


class AssetsHighEndDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsHighEndDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_trade_detail_page(self):
        self.perform_actions(TRADE_DETAIL)
        page = TradeDetailPage(self.web_driver)
        return page

    @robot_log
    def view_high_end_more_product(self):
        self.perform_actions(
            HIGH_END_MORE_PRODUCT,
        )

    @robot_log
    def view_high_end_history_product(self):
        self.perform_actions(
            HIGH_END_MORE_PRODUCT,
            HIGH_END_START, HISTORY_PRODUCT_STOP, 'U',
            HISTORY_PRODUCT,
        )

    @robot_log
    def redeem_high_end_product(self, redeem_amount, trade_password, high_end_product):
        self.perform_actions(
            TITLE_START, HIGH_END_PRODUCT_STOP % high_end_product, 'U',
            HIGH_END_PRODUCT % high_end_product,
            REDEEM,
            REDEEM_AMOUNT_2, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
            REDEEM_DONE,
        )

        page = self

        return page

    @robot_log
    def normal_redeem_vipproduct(self, redeem_amount, trade_password, high_end_product_for_fast_redeem):
        self.perform_actions(
            TITLE_START, HIGH_END_PRODUCT_STOP % high_end_product_for_fast_redeem, 'U',
            HIGH_END_PRODUCT % high_end_product_for_fast_redeem,
            REDEEM,
            NORMAL_REDEEM,
            NORMAL_REDEEM_VIPPRODUCT_AMOUNT, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
            REDEEM_DONE,
        )

        page = self

        return page

    @robot_log
    def fast_redeem_vipproduct(self, redeem_amount, trade_password, high_end_product_for_fast_redeem):
        self.perform_actions(
            TITLE_START, HIGH_END_PRODUCT_STOP % high_end_product_for_fast_redeem, 'U',
            HIGH_END_PRODUCT % high_end_product_for_fast_redeem,
            REDEEM,
            FAST_REDEEM,
            REDEEM_AMOUNT, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
            REDEEM_DONE,
        )

        page = self

        return page
