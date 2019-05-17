# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_redeem_page
import huaxin_ui.ui_ios_xjb_3_0.product_purchase_page
import huaxin_ui.ui_ios_xjb_3_0.product_detail_page

SOLD_OUT = "accId_UIAButton_卖出"
PRODUCT_DETAIL = "accId_UIAStaticTex_查看产品详情"
SUPPLEMENTARY_PURCHASE = "accId_UIAButton_追加"


class DhbHoldingDetailPage(PageObject):
    def __init__(self, web_driver):
        super(DhbHoldingDetailPage, self).__init__(web_driver)

    @robot_log
    def go_to_fund_redeem_page(self):
        self.perform_actions(SOLD_OUT)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_redeem_page.FundRedeemPage(self.web_driver)
        return page

    @robot_log
    def verify_at_dhb_holding_detail_page(self, product_name):
        self.assert_values(product_name, self.get_text("//UIAStaticText[@label='%s']" % product_name))

        page = self
        return page

    @robot_log
    def go_to_product_detail_page(self):
        self.perform_actions(
            PRODUCT_DETAIL
        )

        page = huaxin_ui.ui_ios_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)
        return page

    @robot_log
    def dhb_product_supplementary_purchase(self):
        self.perform_actions(
            SUPPLEMENTARY_PURCHASE
        )

        page = huaxin_ui.ui_ios_xjb_3_0.product_purchase_page.ProductPurchasePage(self.web_driver)
        return page
