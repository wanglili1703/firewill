# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log, user_info_close_afterwards
from huaxin_ui.ui_android_xjb_2_0.fund_more_product_page import FundMoreProductPage
from huaxin_ui.ui_android_xjb_2_0.trade_detail_page import TradeDetailPage

TRADE_DETAIL = "xpath_//android.widget.Button[@text='交易记录']"
FUND_MORE_PRODUCT = "xpath_//android.widget.Button[@text='查看更多产品']"
REDEEM = "xpath_//android.widget.Button[@text='卖出']"
REDEEM_AMOUNT = "xpath_//android.widget.EditText[@text='输入份额']"
REDEEM_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
REDEEM_DONE = "xpath_//android.widget.Button[@text='确认']"

TITLE_START = "swipe_xpath_//"
FUND_PRODUCT_STOP = "swipe_xpath_//*[contains(@text,'%s')]"
FUND_PRODUCT = "xpath_//*[contains(@text,'%s')]"
NORMAL_REDEEM="xpath_//android.widget.RadioButton[@resource-id='com.shhxzq.xjb:id/rbtn_redeem_normal_select']"
FAST_REDEEM="xpath_//android.widget.RadioButton[@resource-id='com.shhxzq.xjb:id/rbtn_redeem_faster_select']"

current_page = []


class AssetsFundDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsFundDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_trade_detail_page(self):
        self.perform_actions(TRADE_DETAIL)
        page = TradeDetailPage(self.web_driver)
        return page

    @robot_log
    @user_info_close_afterwards
    def go_to_fund_more_product_page(self):
        self.perform_actions(
            FUND_MORE_PRODUCT,
        )

        page = FundMoreProductPage(self.web_driver)

        return page

    @robot_log
    def redeem_fund_product(self, fund_product, amount, trade_password):
        self.perform_actions(
            TITLE_START, FUND_PRODUCT_STOP % fund_product, 'U',
            FUND_PRODUCT % fund_product,
            REDEEM,
            REDEEM_AMOUNT, amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
            REDEEM_DONE,
        )

        page = self

        return page

    # 基金普通卖出
    @robot_log
    def normal_redeem_fund_product(self, fund_product_name_for_fast_redeem, redeem_amount, trade_password):
        self.perform_actions(
            TITLE_START, FUND_PRODUCT_STOP % fund_product_name_for_fast_redeem, 'U',
            FUND_PRODUCT % fund_product_name_for_fast_redeem,
            REDEEM,
            NORMAL_REDEEM,
            REDEEM_AMOUNT, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
            REDEEM_DONE,
        )

        page = self

        return page

    # 基金极速卖出
    @robot_log
    def fast_redeem_fund_product(self, fund_product_name_for_fast_redeem, redeem_amount, trade_password):
        self.perform_actions(
            TITLE_START, FUND_PRODUCT_STOP % fund_product_name_for_fast_redeem, 'U',
            FUND_PRODUCT % fund_product_name_for_fast_redeem,
            REDEEM,
            FAST_REDEEM,
            REDEEM_AMOUNT, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
            REDEEM_DONE,
        )

        page = self

        return page