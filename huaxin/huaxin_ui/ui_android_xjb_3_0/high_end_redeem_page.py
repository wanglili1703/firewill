# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.redeem_detail_page
import huaxin_ui.ui_android_xjb_3_0.product_purchase_page
import huaxin_ui.ui_android_xjb_3_0.product_detail_page
import huaxin_ui.ui_android_xjb_3_0.trade_detail_page

REDEEM = "xpath_//android.widget.Button[@text='卖出']"
PRODUCT_DETAIL = "xpath_//android.widget.TextView[@text='查看产品详情']"
SUPPLEMENTARY_PURCHASE = "xpath_//android.widget.Button[@text='追加']"
RECORD = "xpath_//android.widget.TextView[@text='交易记录']"


class HighEndRedeemPage(PageObject):
    def __init__(self, web_driver):
        super(HighEndRedeemPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self, product_name):
        self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_redeem_detail_page(self):
        self.perform_actions(REDEEM)

        page = huaxin_ui.ui_android_xjb_3_0.redeem_detail_page.RedeemDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_product_detail_page(self):
        self.perform_actions(
            PRODUCT_DETAIL
        )

        page = huaxin_ui.ui_android_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)

        return page

    @robot_log
    def vipproduct_supplementary_purchase(self):
        self.perform_actions(
            SUPPLEMENTARY_PURCHASE
        )

        page = huaxin_ui.ui_android_xjb_3_0.product_purchase_page.ProductPurchasePage(self.web_driver)

        return page

    @robot_log
    def go_to_trade_records_page(self):
        self.perform_actions(
            RECORD
        )

        page = huaxin_ui.ui_android_xjb_3_0.trade_detail_page.TradeDetailPage(self.web_driver)

        return page
