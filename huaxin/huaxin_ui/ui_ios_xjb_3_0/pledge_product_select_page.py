# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.pledge_detail_page

current_page = []

PRODUCT_NAME = "accId_UIAStaticText_(%s)"


class PledgeProductSelectPage(PageObject):
    def __init__(self, web_driver):
        super(PledgeProductSelectPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_pledge_product_select_page(self):
        self.assert_values("选择质押产品", self.get_text("//UIAStaticText[@label='选择质押产品']"))

    @robot_log
    def select_pledge_product_page(self, product_name):
        self.perform_actions(PRODUCT_NAME % product_name)

        page = huaxin_ui.ui_ios_xjb_3_0.pledge_detail_page.PledgeDetailPage(self.web_driver)

        return page

