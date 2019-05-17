# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

current_page = []
TRADE_TYPE_LIST = "accId_UIAButton_(UIButton_全部icon_arrowfold_white)"
TRADE_TYPE_DONE = "accId_UIAButton_完成"
TRADE_TYPE_SCROLL_1 = "swipe_accId_scroll_1"
TRADE_TYPE_SCROLL_2 = "swipe_accId_scroll_1"
TRADE_TYPE_SCROLL_3 = "swipe_accId_scroll_1"


class XjbTradeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(XjbTradeDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def view_xjb_trade_detail(self):
        self.perform_actions(
            TRADE_TYPE_LIST,
            TRADE_TYPE_DONE,
            TRADE_TYPE_LIST,
            'swipe_xpath_//', TRADE_TYPE_SCROLL_1, 'U',
            TRADE_TYPE_DONE,
            TRADE_TYPE_LIST,
            'swipe_xpath_//', TRADE_TYPE_SCROLL_2, 'U',
            TRADE_TYPE_DONE,
            TRADE_TYPE_LIST,
            'swipe_xpath_//', TRADE_TYPE_SCROLL_3, 'U',
            TRADE_TYPE_DONE,
        )

        page = self

        return page
