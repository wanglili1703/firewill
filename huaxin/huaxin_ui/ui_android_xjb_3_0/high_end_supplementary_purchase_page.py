# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.product_detail_page
PRODUCT_DETAIL = "xpath_//android.widget.TextView[@text='查看产品详情']"

class HighEndSupplementaryPurchasePage(PageObject):
    def __init__(self, web_driver):
        super(HighEndSupplementaryPurchasePage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self, product_name):
        self.assert_values(product_name, self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_high_end_supplementary_purchase_page_details(self, amount):
        self.assert_values('购买确认中', self.get_text('com.shhxzq.xjb:id/tv_vip_details_validdate', 'find_element_by_id'))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='购买金额(元)']")))
        self.assert_values('%.2f' % float(amount), self.get_text(
            "//android.widget.TextView[@text='购买金额(元)']/following-sibling::android.widget.LinearLayout/android.widget.TextView"))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='查看产品详情']")))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='交易记录']")))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='开放说明']")))

        page = self

        return page

    @robot_log
    def go_to_product_detail_page(self):
        self.perform_actions(PRODUCT_DETAIL)

        page = huaxin_ui.ui_android_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)

        return page

