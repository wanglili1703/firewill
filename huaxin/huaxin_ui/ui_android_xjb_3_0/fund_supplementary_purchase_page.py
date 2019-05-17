# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_purchase_page

SUPPLEMENTARY_PURCHASE = "xpath_//android.widget.Button[@text='继续买入']"


class FundSupplementaryPurchasePage(PageObject):
    def __init__(self, web_driver):
        super(FundSupplementaryPurchasePage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self, fund_product):
        self.assert_values(fund_product, self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_fund_purchase_result(self, amount):
        self.assert_values('%.2f' % float(amount), self.get_text('com.shhxzq.xjb:id/content', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_fund_supplementary_purchase_page_details(self, fund_product):
        self.assert_values('购买确认中', self.get_text('com.shhxzq.xjb:id/tv_fund_details_validdate', 'find_element_by_id'))
        self.assert_values(fund_product, self.get_text('com.shhxzq.xjb:id/tv_fund_details_nm', 'find_element_by_id'))
        self.assert_values('产品详情', self.get_text('com.shhxzq.xjb:id/tv_fund_details_detail', 'find_element_by_id'))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='购买金额(元)']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='交易记录']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='定投计划']"))

        page = self
        return page

    @robot_log
    def fund_supplementary_purchase(self):
        self.perform_actions(
            SUPPLEMENTARY_PURCHASE
        )

        page = huaxin_ui.ui_android_xjb_3_0.fund_purchase_page.FundPurchasePage(self.web_driver)

        return page
