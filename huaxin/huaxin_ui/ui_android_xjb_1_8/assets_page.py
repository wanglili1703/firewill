# coding: utf-8

from _common.page_object import PageObject

IDENTIFIER = "xpath_//android.widget.TextView[@text='我的资产']"
CARD_MANAGEMENT_BUTTON = "xpath_//android.widget.TextView[@text='银行卡管理']"
XJB_BUTTON = "xpath_//android.widget.TextView[@text='现金宝']"
REGULAR_BUTTON = "xpath_//android.widget.TextView[@text='定期宝']"
HIGH_END_BUTTON = "xpath_//android.widget.TextView[@text='高端理财']"
CREDIT_CARD_REPAY_BUTTON = "xpath_//android.widget.TextView[@text='信用卡还款']"
TRADE_RECORD_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_right']"

current_page = []


class AssetsPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
