# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.my_coupons_list_page

TITLE_ELE = "//UIAStaticText[@label='商品详情']"
EXCHANGE = "xpathIOS_UIAButton_//UIAButton[@label='立即兑换']"
GO_TO_USE = "xpathIOS_UIAButton_//UIAButton[@label='去使用']"
CONFIRM = "xpathIOS_UIAButton_//UIAButton[@label='确定']"
CONSUME_QUANTITY = "xpathIOS_UIAButton_//UIAButton[@label='3积分+6元宝']"
current_page = []


class GoodsDetailPage(PageObject):
    def __init__(self, web_driver):
        super(GoodsDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
        }

    @robot_log
    def verify_at_goods_details_page(self):
        title = self.get_text(TITLE_ELE)
        self.assert_values('商品详情', title)

    @robot_log
    def exchange_immediately(self):
        self.verify_at_goods_details_page()

        self.perform_actions(CONSUME_QUANTITY,
                             EXCHANGE)

        self.perform_actions(CONFIRM)

        self.perform_actions(GO_TO_USE)

        page = huaxin_ui.ui_ios_xjb_3_0.my_coupons_list_page.MyCouponsListPage(self.web_driver)
        return page
