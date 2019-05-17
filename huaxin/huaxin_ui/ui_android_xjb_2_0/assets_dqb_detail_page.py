# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_android_xjb_2_0.trade_detail_page import TradeDetailPage

TRADE_DETAIL = "xpath_//android.widget.Button[@text='交易查询']"
DQB_MORE_PRODUCT = "xpath_//android.widget.TextView[@text='查看更多产品']"

DQB_START = "swipe_xpath_//android.widget.TextView[@text='定期']"
HISTORY_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='查看历史产品']"
HISTORY_PRODUCT = "xpath_//android.widget.TextView[@text='查看历史产品']"

TITLE_START = "swipe_xpath_//android.widget.TextView[@text='定期宝']"
DQB_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
DQB_PRODUCT = "xpath_//android.widget.TextView[@text='%s']"
REDEEM = "xpath_//android.widget.Button[@text='取回']"
REDEEM_AMOUNT = "xpath_//android.widget.EditText[@text='请输入取回金额']"
REDEEM_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
REDEEM_DONE = "xpath_//android.widget.Button[@text='确认']"

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

        page = self

        return page
