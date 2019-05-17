# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.pledge_detail_page
PLEDGE_PRODUCT = "xpath_//android.widget.TextView[@text='%s']"

class SelectpledgeProductPage(PageObject):
    def __init__(self, web_driver):
        super(SelectpledgeProductPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('选择质押产品', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def go_to_pledge_detail_page(self,product_name):
        self.perform_actions(PLEDGE_PRODUCT % product_name)

        page = huaxin_ui.ui_android_xjb_3_0.pledge_detail_page.PledgeDetailPage(self.web_driver)
        return page
