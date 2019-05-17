# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_product_search_page
import huaxin_ui.ui_android_xjb_3_0.fund_selected_fund_management_page

FUND_PRODUCT_SEARCH = "xpath_//android.widget.TextView[@text='基金代码/简拼/重仓资产']"
NAMAGEMENT = "xpath_//android.widget.TextView[@text='管理']"


class FundSelectedPage(PageObject):
    def __init__(self, web_driver):
        super(FundSelectedPage, self).__init__(web_driver)

    @robot_log
    def go_to_fund_product_search_page(self):
        self.perform_actions(FUND_PRODUCT_SEARCH)

        page = huaxin_ui.ui_android_xjb_3_0.fund_product_search_page.FundProductSearchPage(self.web_driver)

        return page

    @robot_log
    def verify_selected_fund_details(self, fund_product_name, fund_product_code):
        self.assert_values(fund_product_name, self.get_text('com.shhxzq.xjb:id/title', 'find_element_by_id'))
        self.assert_values(fund_product_code, self.get_text('com.shhxzq.xjb:id/fund_code', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_selected_fund_management_page(self):
        self.perform_actions(NAMAGEMENT)

        page = self

        return page

    @robot_log
    def go_to_selected_fund_management_page(self):
        self.perform_actions(NAMAGEMENT)

        page = huaxin_ui.ui_android_xjb_3_0.fund_selected_fund_management_page.FundSelectedFundManagementPage(
            self.web_driver)

        return page

    @robot_log
    def verify_no_selected_fund(self, fund_product_name, fund_product_code):
        self.assert_values('False',
                           str(self.element_exist("//android.widget.TextView[@text='%s']" % fund_product_name)))
        self.assert_values('False',
                           str(self.element_exist("//android.widget.TextView[@text='%s']" % fund_product_code)))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='暂无自选基金，点击添加']")))

        page = self
        return page
