# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.assets_page

current_page = []
TRADE_TYPE_LIST = "accId_UIAButton_(UIButton_全部icon_arrowfold)"
TRADE_TYPE_DONE = "accId_UIAButton_完成"
TRADE_TYPE_SCROLL_1 = "swipe_accId_scroll_1"
TRADE_TYPE_SCROLL_2 = "swipe_accId_scroll_1"
TRADE_TYPE_SCROLL_3 = "swipe_accId_scroll_1"

BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"


class DhbTradeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(DhbTradeDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_trade_detail_page(self):
        title = self.get_text("//UIAStaticText[@label='交易记录']")
        self.assert_values('交易记录', title)

    @robot_log
    def view_dhb_trade_detail(self):
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

    @robot_log
    def go_to_assets_page(self):
        self.perform_actions(BACK,
                             BACK,
                             )

        page = huaxin_ui.ui_ios_xjb_3_0.assets_page.AssetsPage(self.web_driver)

        return page
