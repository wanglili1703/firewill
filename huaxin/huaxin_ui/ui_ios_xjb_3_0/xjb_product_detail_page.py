# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
PERFORMANCE = "accId_UIAButton_(UIButton_业绩)"
PERFORMANCE = "accId_UIAButton_(UIButton_业绩)"

class XjbProductDetailPage(PageObject):
    def __init__(self, web_driver):
        super(XjbProductDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_at_xjb_product_detail_page(self):
        self.assert_values('基金详情', self.get_text("//UIAStaticText[@label='基金详情']"))

        page = self

        return page

    @robot_log
    def verify_xjb_product_details(self):
        self.assert_values('业绩', self.get_text("accId_UIAButton_(UIButton_业绩)"))
        self.assert_values('概况', self.get_text("//UIAStaticText[@label='概况']"))
        self.assert_values('组合', self.get_text("//UIAStaticText[@label='组合']"))
        self.assert_values('费率', self.get_text("//UIAStaticText[@label='费率']"))
        self.assert_values('公告', self.get_text("//UIAStaticText[@label='公告']"))
        self.assert_values('立即存入', self.get_text('立即存入', 'find_element_by_accessibility_id'))

        page = self

        return page
