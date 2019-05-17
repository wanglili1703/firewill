# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_android_xjb_3_0.assets_specific_trade_detail_page

current_page = []
TRADE_TYPE_LIST = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/filter_type']"
TRADE_TYPE_ALL = "xpath_//android.widget.CheckedTextView[@text='全部产品']"
TRADE_TYPE_XJB = "xpath_//android.widget.CheckedTextView[@text='现金宝']"
TRADE_TYPE_DQB = "xpath_//android.widget.CheckedTextView[@text='定活宝']"
TRADE_TYPE_HIGH_END = "xpath_//android.widget.CheckedTextView[@text='高端理财']"
TRADE_TYPE_FUND = "xpath_//android.widget.CheckedTextView[@text='基金']"

TRADE_STATUS_LIST = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/filter_status']"
TRADE_STATUS_ALL = "xpath_//android.widget.CheckedTextView[@text='全部状态']"
TRADE_STATUS_SUCESS = "xpath_//android.widget.CheckedTextView[@text='成功']"
TRADE_STATUS_DOING = "xpath_//android.widget.CheckedTextView[@text='已受理／处理中']"
TRADE_STATUS_FAIL = "xpath_//android.widget.CheckedTextView[@text='失败']"
TRADE_STATUS_CANCEL = "xpath_//android.widget.CheckedTextView[@text='已撤消']"
TRADE_RECORD = "xpath_//android.widget.TextView[contains(@text,'%s')]"
SWIPE_BEGIN = "swipe_xpath_//"
PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
TRADE_TYPE = "xpath_//android.widget.TextView[@text='买入']"


class TradeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(TradeDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('交易记录', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def view_trade_detail(self):
        self.perform_actions(
            TRADE_TYPE_LIST,
            TRADE_TYPE_XJB,
            TRADE_TYPE_LIST,
            TRADE_TYPE_DQB,
            TRADE_TYPE_LIST,
            TRADE_TYPE_HIGH_END,
            TRADE_TYPE_LIST,
            TRADE_TYPE_FUND,
            TRADE_TYPE_LIST,
            TRADE_TYPE_ALL,
            TRADE_STATUS_LIST,
            TRADE_STATUS_ALL,
            TRADE_STATUS_LIST,
            TRADE_STATUS_SUCESS,
            TRADE_STATUS_LIST,
            TRADE_STATUS_DOING,
            TRADE_STATUS_LIST,
            TRADE_STATUS_FAIL,
            TRADE_STATUS_LIST,
            TRADE_STATUS_CANCEL,
        )

        page = self

        return page

    @robot_log
    def verify_trade_details(self, trade_type, status, amount=None, product_name=None):

        self.assert_values(trade_type, self.get_text('com.shhxzq.xjb:id/trade_type', 'find_element_by_id'))
        if product_name is not None:
            self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/trade_desp', 'find_element_by_id'))

        self.assert_values(status, self.get_text('com.shhxzq.xjb:id/status', 'find_element_by_id'))
        amount_text = self.get_text('com.shhxzq.xjb:id/trade_amount', 'find_element_by_id')
        amount_actual = '%.2f' % float(filter(lambda ch: ch in '0123456789.', amount_text))
        if trade_type == '取回':
            self.assert_values('%.2f' % float(ASSERT_DICT['redeem_amount']), amount_actual)
        elif amount is not None:
            self.assert_values('%.2f' % float(amount), amount_actual)

        page = self
        return page

    @robot_log
    def go_to_specific_trade_detail_page(self, product_name):
        self.perform_actions(SWIPE_BEGIN, PRODUCT_STOP % product_name, 'U')
        self.perform_actions(TRADE_RECORD % product_name)

        page = huaxin_ui.ui_android_xjb_3_0.assets_specific_trade_detail_page.AssetsSpecificTradeDetailPage(
            self.web_driver)
        return page

    @robot_log
    def select_filter_type(self, filter_type=None):
        if filter_type == 'fund':
            self.perform_actions(TRADE_TYPE_LIST,
                                 TRADE_TYPE_FUND)
        elif filter_type == 'dhb':
            self.perform_actions(TRADE_TYPE_LIST,
                                 TRADE_TYPE_DQB)

        page = self
        return page
