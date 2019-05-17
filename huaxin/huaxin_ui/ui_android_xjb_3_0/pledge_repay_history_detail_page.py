# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT

class PledgeRepayHistoryDetailPage(PageObject):
    def __init__(self, web_driver):
        super(PledgeRepayHistoryDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('还款详情', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_pledge_repay_history_details(self,product_name,pledge_repay_amount):
        self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/tv_mortgage_product', 'find_element_by_id'))
        self.assert_values('0.00', self.get_text('com.shhxzq.xjb:id/tv_mortgage_percent', 'find_element_by_id'))
        self.assert_values('%.2f' % float(pledge_repay_amount), self.get_text('com.shhxzq.xjb:id/tv_had_repay_principal', 'find_element_by_id'))
        self.assert_values(ASSERT_DICT['interest'], self.get_text('com.shhxzq.xjb:id/tv_had_repay_interest', 'find_element_by_id'))

        page = self
        return page


