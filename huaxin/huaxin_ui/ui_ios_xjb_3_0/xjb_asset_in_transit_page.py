# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log


class XjbAssetInTransitPage(PageObject):
    def __init__(self, web_driver):
        super(XjbAssetInTransitPage, self).__init__(web_driver)

    @robot_log
    def verify_at_assets_in_transit_page(self):
        self.assert_values('在途资产', self.get_text("//UIAStaticText[@label='在途资产']"))

        page = self
        return page

    @robot_log
    def verify_asset_in_transit_details(self):
        self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, '在途资金：')]"))
        self.assert_values('现金宝', self.get_text("现金宝", "find_element_by_accessibility_id"))

        page = self
        return page
