# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

current_page = []
TRADE_TYPE_LIST = "accId_UIAButton_(btnFilterType)"
TRADE_TYPE_DONE = "accId_UIAButton_完成"

SWIPE_BEGAIN = "swipe_xpath_//"

TRADE_TYPE_SCROLL_1 = "swipe_accId_scroll_1"
TRADE_TYPE_SCROLL_2 = "swipe_accId_scroll_1"
TRADE_TYPE_SCROLL_3 = "swipe_accId_scroll_1"
TRADE_TYPE_SCROLL_4 = "swipe_accId_scroll_1"

TRADE_STATUS_LIST = "accId_UIAButton_(btnFilterStatus)"
TRADE_STATUS_DONE = "accId_UIAButton_完成"
TRADE_STATUS_SCROLL_1 = "swipe_accId_scroll_1"
TRADE_STATUS_SCROLL_2 = "swipe_accId_scroll_1"
TRADE_STATUS_SCROLL_3 = "swipe_accId_scroll_1"
TRADE_STATUS_SCROLL_4 = "swipe_accId_scroll_1"


class TradeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(TradeDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def view_trade_detail(self):
        self.perform_actions(
            TRADE_TYPE_LIST,
            TRADE_TYPE_DONE,
            TRADE_TYPE_LIST,
            SWIPE_BEGAIN, TRADE_TYPE_SCROLL_1, 'U',
            TRADE_TYPE_DONE,
            # TRADE_TYPE_LIST,
            # SWIPE_BEGAIN, TRADE_TYPE_SCROLL_2, 'U',
            # TRADE_TYPE_DONE,
            # TRADE_TYPE_LIST,
            # SWIPE_BEGAIN, TRADE_TYPE_SCROLL_3, 'U',
            # TRADE_TYPE_DONE,
            # TRADE_TYPE_LIST,
            # SWIPE_BEGAIN, TRADE_TYPE_SCROLL_4, 'U',
            # TRADE_TYPE_DONE,
            TRADE_STATUS_LIST,
            TRADE_STATUS_DONE,
            TRADE_STATUS_LIST,
            SWIPE_BEGAIN, TRADE_STATUS_SCROLL_1, 'U',
            TRADE_STATUS_DONE,
            # TRADE_STATUS_LIST,
            # SWIPE_BEGAIN, TRADE_STATUS_SCROLL_2, 'U',
            # TRADE_STATUS_DONE,
            # TRADE_STATUS_LIST,
            # SWIPE_BEGAIN, TRADE_STATUS_SCROLL_3, 'U',
            # TRADE_STATUS_DONE,
            # TRADE_STATUS_LIST,
            # SWIPE_BEGAIN, TRADE_STATUS_SCROLL_4, 'U',
            # TRADE_STATUS_DONE,
        )

        page = self

        return page
