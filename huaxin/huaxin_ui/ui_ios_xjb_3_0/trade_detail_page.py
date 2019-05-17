# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.trade_record_detail_page

current_page = []
TRADE_TYPE_LIST = "xpathIOS_UIAButton_//UIAButton[@label='定活宝']"
TRADE_TYPE_DONE = "accId_UIAButton_完成"

SWIPE_BEGAIN = "swipe_xpath_//"

TRADE_TYPE_SCROLL_1 = "swipe_accId_scroll_1"
TRADE_TYPE_SCROLL_2 = "swipe_accId_scroll_1"
TRADE_TYPE_SCROLL_3 = "swipe_accId_scroll_1"
TRADE_TYPE_SCROLL_4 = "swipe_accId_scroll_1"

TRADE_STATUS_LIST = "xpathIOS_UIAButton_//UIAButton[@label='全部状态']"
TRADE_STATUS_DONE = "accId_UIAButton_完成"
TRADE_STATUS_SCROLL_1 = "swipe_accId_scroll_1"
TRADE_STATUS_SCROLL_2 = "swipe_accId_scroll_1"
TRADE_STATUS_SCROLL_3 = "swipe_accId_scroll_1"
TRADE_STATUS_SCROLL_4 = "swipe_accId_scroll_1"
RECORD = "xpathIOS_UIAStaticText_//UIATableCell[@name='(tradeList)' and @visible='true']/UIAStaticText[1]"
TRADE_RECORD = "accId_UIAStaticText_(%s)"


class TradeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(TradeDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_trade_detail_page(self):
        title = self.get_text("//UIAStaticText[@label='交易记录']")
        self.assert_values('交易记录', title)

    @robot_log
    def view_trade_detail(self, default_type='定活宝', default_status='全部状态'):
        # 验证从定活宝交易记录进来显示默认的为定活宝和全部状态
        self.assert_values(True, self.element_exist("//UIAButton[@label='%s']" % default_type))
        self.assert_values(True, self.element_exist("//UIAButton[@label='%s']" % default_status))

        page = self
        return page

    @robot_log
    def switch_to_other_trade_type_record(self, trade_type, status):
        # to do

        page = self

        return page

    @robot_log
    def go_to_trade_record_detail_page(self):
        self.perform_actions(RECORD)
        page = huaxin_ui.ui_ios_xjb_3_0.trade_record_detail_page.TradeRecordDetailPage(self.web_driver)
        return page

    @robot_log
    def go_to_specific_trade_detail_page(self, product_name):
        self.perform_actions(TRADE_RECORD % product_name)

        page = huaxin_ui.ui_ios_xjb_3_0.trade_record_detail_page.TradeRecordDetailPage(
            self.web_driver)
        return page
