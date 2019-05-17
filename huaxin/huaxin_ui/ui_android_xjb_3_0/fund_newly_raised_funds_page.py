# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail

STATUS = "//android.widget.TextView[@text='%s']/following-sibling::android.widget.TextView[1]"
FUND_CODE = "//android.widget.TextView[@text='%s']/../following-sibling::android.widget.LinearLayout[1]/android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_fund_number']"
FUND_RAISE_CIRCLE = "//android.widget.TextView[@text='%s']/../following-sibling::android.widget.LinearLayout[1]/android.widget.TextView[contains(@text,'募集结束')]"
FUND = "xpath_//android.widget.TextView[@text='%s']"


class FundNewlyRaisedFundsPage(PageObject):
    def __init__(self, web_driver):
        super(FundNewlyRaisedFundsPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('新发基金', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_newly_raised_fund_details(self, product_name):
        self.assert_values('募集中', self.get_text(STATUS % product_name))
        self.assert_values('050033', self.get_text(FUND_CODE % product_name))
        self.assert_values(True, self.element_exist(FUND_RAISE_CIRCLE % product_name))

        page = self
        return page

    @robot_log
    def go_to_fund_detail_page(self, product_name):
        self.perform_actions(FUND % product_name)

        page = huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)
        return page
