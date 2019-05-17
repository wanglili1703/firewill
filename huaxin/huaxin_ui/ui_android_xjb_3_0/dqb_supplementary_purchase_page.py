# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.product_purchase_page
import huaxin_ui.ui_android_xjb_3_0.product_detail_page

SUPPLEMENTARY_PURCHASE = "xpath_//android.widget.Button[@text='追加']"
PRODUCT_DETAIL = "xpath_//android.widget.TextView[@text='查看产品详情']"


class DqbSupplementaryPurchasePage(PageObject):
    def __init__(self, web_driver):
        super(DqbSupplementaryPurchasePage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self, product_name):
        self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_dqb_supplementary_purchase_page_details(self, product_name, amount=None):
        self.assert_values('购买确认中', self.get_text('com.shhxzq.xjb:id/dqb_details_validdate', 'find_element_by_id'))
        self.assert_values(product_name, self.get_text(self.page_title, 'find_element_by_id'))
        self.assert_values('购买金额(元)', self.get_text('com.shhxzq.xjb:id/purchase_amount_title', 'find_element_by_id'))
        if amount is not None:
            self.assert_values('%.2f' % float(amount),
                               self.get_text('com.shhxzq.xjb:id/purchase_amount', 'find_element_by_id'))
        self.assert_values('当前累计收益(元)', self.get_text('com.shhxzq.xjb:id/total_income_title', 'find_element_by_id'))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='查看产品详情']")))

        page = self
        return page

    @robot_log
    def dqb_supplementary_purchase(self):
        self.perform_actions(
            SUPPLEMENTARY_PURCHASE
        )

        page = huaxin_ui.ui_android_xjb_3_0.product_purchase_page.ProductPurchasePage(self.web_driver)

        return page

    @robot_log
    def go_to_product_detail_page(self):
        self.perform_actions(PRODUCT_DETAIL)

        page = huaxin_ui.ui_android_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)

        return page
