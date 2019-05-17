# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

current_page = []
TRADE_TYPE_LIST = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/filter_type']"
TRADE_TYPE_ALL = "xpath_//android.widget.CheckedTextView[@text='全部产品']"
TRADE_TYPE_XJB = "xpath_//android.widget.CheckedTextView[@text='现金宝']"
TRADE_TYPE_DQB = "xpath_//android.widget.CheckedTextView[@text='定期宝']"
TRADE_TYPE_HIGH_END = "xpath_//android.widget.CheckedTextView[@text='高端理财']"
TRADE_TYPE_FUND = "xpath_//android.widget.CheckedTextView[@text='基金']"

TRADE_STATUS_LIST = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/filter_status']"
TRADE_STATUS_ALL = "xpath_//android.widget.CheckedTextView[@text='全部状态']"
TRADE_STATUS_SUCESS = "xpath_//android.widget.CheckedTextView[@text='成功']"
TRADE_STATUS_DOING = "xpath_//android.widget.CheckedTextView[@text='已受理／处理中']"
TRADE_STATUS_FAIL = "xpath_//android.widget.CheckedTextView[@text='失败']"
TRADE_STATUS_CANCEL = "xpath_//android.widget.CheckedTextView[@text='已撤消']"


class TradeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(TradeDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

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
