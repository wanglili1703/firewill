# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_2_0.trade_detail_page import TradeDetailPage
import huaxin_ui.ui_ios_xjb_2_0.assets_page

TRADE_DETAIL = "accId_UIAButton_交易记录"
DQB_MORE_PRODUCT = "accId_UIAButton_查看更多产品"

DQB_START = "swipe_accId_定期"
HISTORY_PRODUCT_STOP = "swipe_accId_查看历史产品"
HISTORY_PRODUCT = "accId_UIAButton_查看历史产品"

TITLE_START = "swipe_accId_定期宝"
DQB_PRODUCT_STOP = "swipe_accId_%s"
DQB_PRODUCT = "accId_UIAStaticText_%s"
REDEEM = "accId_UIAButton_取回"
REDEEM_AMOUNT = "accId_UIATextField_(textField)请输入取回金额"
REDEEM_CONFIRM = "accId_UIAButton_确认"
TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
REDEEM_DONE = "accId_UIAButton_确认"

current_page = []


class AssetsDqbDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsDqbDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_trade_detail_page(self):
        self.perform_actions(TRADE_DETAIL)
        page = TradeDetailPage(self.web_driver)
        return page

    @robot_log
    def view_dqb_more_product(self):
        self.perform_actions(
            DQB_MORE_PRODUCT,
        )

    @robot_log
    def view_dqb_history_product(self):
        self.perform_actions(
            DQB_MORE_PRODUCT,
            DQB_START, HISTORY_PRODUCT_STOP, 'U',
            HISTORY_PRODUCT,
        )

    @robot_log
    def redeem_dqb_product(self, redeem_amount, trade_password, dqb_product):
        self.perform_actions(
            TITLE_START, DQB_PRODUCT_STOP % dqb_product, 'U',
            DQB_PRODUCT % dqb_product,
            REDEEM,
            REDEEM_AMOUNT, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
            REDEEM_DONE,
        )

        page = huaxin_ui.ui_ios_xjb_2_0.assets_page.AssetsPage(self.web_driver)

        return page
