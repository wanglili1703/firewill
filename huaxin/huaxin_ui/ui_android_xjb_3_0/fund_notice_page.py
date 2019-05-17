# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"


class FundNoticePage(PageObject):
    def __init__(self, web_driver):
        super(FundNoticePage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('基金公告', self.get_text(self.page_title, 'find_element_by_id'))
        page = self

        return page

    @robot_log
    def back_to_product_detail_page(self):
        self.perform_actions(BACK)
        page = huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)

        return page

