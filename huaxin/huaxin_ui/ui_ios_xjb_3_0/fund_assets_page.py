# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_assets_structure_page

BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"
TRADE_RECORD = "accId_UIAButton_UIBarButtonItemLocationRight"
FUND_PRODUCT = "accId_UIAStaticText_%s"


class FundAssetsPage(PageObject):
    def __init__(self, web_driver):
        super(FundAssetsPage, self).__init__(web_driver)

    @robot_log
    def verify_at_fund_assets_page(self):
        self.assert_values('基金资产', self.get_text("//UIAStaticText[@label='基金资产']"))

        page = self
        return page

    @robot_log
    def verify_fund_assets_details(self, fund_type):
        self.assert_values(fund_type + '基金总资产(元)',
                           self.get_text('(%s基金总资产(元))' % fund_type, "find_element_by_accessibility_id"))
        self.assert_values(True, self.element_exist("(最新收益(元))", "find_element_by_accessibility_id"))
        self.assert_values(True, self.element_exist("(累计收益(元))", "find_element_by_accessibility_id"))

        page = self
        return page

    @robot_log
    def back_to_fund_assets_structure_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_assets_structure_page.FundAssetsStructurePage(self.web_driver)
        return page

    @robot_log
    def go_to_fund_holding_details_page(self, product_name):
        self.perform_actions(FUND_PRODUCT % product_name)
