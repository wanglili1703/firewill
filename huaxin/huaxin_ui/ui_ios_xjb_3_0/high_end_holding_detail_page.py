# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_redeem_page
import huaxin_ui.ui_ios_xjb_3_0.product_purchase_page
import huaxin_ui.ui_ios_xjb_3_0.product_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_high_end_detail_page
import huaxin_ui.ui_ios_xjb_3_0.trade_detail_page

SOLD_OUT = "accId_UIAButton_卖出"
PRODUCT_DETAIL = "accId_UIAStaticTex_查看产品详情"
SUPPLEMENTARY_PURCHASE = "accId_UIAButton_追加"
BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"
TRADE_RECORD = "accId_UIAStaticText_交易记录"
BUY_CONTINUE = "accId_UIAButton_继续买入"


class HighEndHoldingDetailPage(PageObject):
    def __init__(self, web_driver):
        super(HighEndHoldingDetailPage, self).__init__(web_driver)
        self._return_page = {
            "AssetsHighEndDetailPage": huaxin_ui.ui_ios_xjb_3_0.assets_high_end_detail_page.AssetsHighEndDetailPage(
                self.web_driver)
        }

    @robot_log
    def go_to_fund_redeem_page(self):
        self.perform_actions(SOLD_OUT)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_redeem_page.FundRedeemPage(self.web_driver)
        return page

    @robot_log
    def back_to_previous_page(self, return_page):
        self.perform_actions(BACK)

        page = self._return_page[return_page]
        return page

    @robot_log
    def verify_at_vip_holding_detail_page(self, product_name):
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
    def go_to_trade_record_page(self):
        self.perform_actions(
            TRADE_RECORD
        )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_detail_page.TradeDetailPage(self.web_driver)
        return page

    @robot_log
    def vip_product_supplementary_purchase(self):
        self.perform_actions(
            SUPPLEMENTARY_PURCHASE
        )

        if self.element_exist(u'风险提示', 'find_element_by_accessibility_id'):
            self.perform_actions(
                BUY_CONTINUE,
            )

        page = huaxin_ui.ui_ios_xjb_3_0.product_purchase_page.ProductPurchasePage(self.web_driver)
        return page
