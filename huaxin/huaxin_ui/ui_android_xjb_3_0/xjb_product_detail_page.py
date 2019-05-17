# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log


class XjbProductDetailPage(PageObject):
    def __init__(self, web_driver):
        super(XjbProductDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('现金宝详情', self.get_text('com.shhxzq.xjb:id/actionbar_title', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_xjb_product_details(self):
        self.assert_values('业绩', self.get_text("//android.widget.TextView[@text='业绩']"))
        self.assert_values('概况', self.get_text("//android.widget.TextView[@text='概况']"))
        self.assert_values('组合', self.get_text("//android.widget.TextView[@text='组合']"))
        self.assert_values('费率', self.get_text("//android.widget.TextView[@text='费率']"))
        self.assert_values('公告', self.get_text("//android.widget.TextView[@text='公告']"))
        self.assert_values('立即存入', self.get_text('com.shhxzq.xjb:id/btn_foot_recharge', 'find_element_by_id'))

        page = self

        return page

