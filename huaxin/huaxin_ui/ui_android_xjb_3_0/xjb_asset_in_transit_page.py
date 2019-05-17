# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log


class XjbAssetInTransitPage(PageObject):
    def __init__(self, web_driver):
        super(XjbAssetInTransitPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('在途资产', self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_asset_in_transit_details(self):
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='在途资金:']")))
        self.assert_values('现金宝', self.get_text('com.shhxzq.xjb:id/tv_top_title', 'find_element_by_id'))
        self.assert_values('True', str(self.element_exist("//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_transit_tips']")))

        page = self

        return page


