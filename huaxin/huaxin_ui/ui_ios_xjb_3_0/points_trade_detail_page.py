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

# POINT_DETAILS = "accId_UIAButton_积分明细"
POINT_DETAILS = "accId_UIAButton_UIBarButtonItemLocationRight"
TYPES_LISTS = "accId_UIAButton_(titleView)"
POINT_STATUS_DONE = "accId_UIAButton_完成"
POINT_TYPE_SCROLL_1 = "swipe_accId_scroll_1"
POINT_TYPE_SCROLL_2 = "swipe_accId_scroll_1"


class PointsTradeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(PointsTradeDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def view_points_trade_detail(self):
        self.perform_actions(POINT_DETAILS,
                             TYPES_LISTS,
                             POINT_STATUS_DONE,
                             TYPES_LISTS,
                             'swipe_xpath_//', POINT_TYPE_SCROLL_1, 'U',
                             POINT_STATUS_DONE,
                             TYPES_LISTS,
                             'swipe_xpath_//', POINT_TYPE_SCROLL_2, 'U',
                             POINT_STATUS_DONE,
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
