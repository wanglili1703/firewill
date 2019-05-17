# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log, user_info_close_afterwards, \
    gesture_close_afterwards
from huaxin_ui.ui_android_xjb_2_0.register_page import RegisterPage

import huaxin_ui.ui_android_xjb_2_0.home_page

current_page = []
TRADE_TYPE_LIST = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/title_actionbar']"
TRADE_TYPE_ALL = "xpath_//android.widget.CheckedTextView[@text='全部']"
TRADE_TYPE_RECHARGE = "xpath_//android.widget.CheckedTextView[@text='存入']"
TRADE_TYPE_WITHDRAW = "xpath_//android.widget.CheckedTextView[@text='取出']"
TRADE_TYPE_INCOME = "xpath_//android.widget.CheckedTextView[@text='收益']"


class XjbTradeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(XjbTradeDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def view_xjb_trade_detail(self):
        self.perform_actions(
            TRADE_TYPE_LIST,
            TRADE_TYPE_ALL,
            TRADE_TYPE_LIST,
            TRADE_TYPE_RECHARGE,
            TRADE_TYPE_LIST,
            TRADE_TYPE_WITHDRAW,
            TRADE_TYPE_LIST,
            TRADE_TYPE_INCOME,
        )

        page = self

        return page
