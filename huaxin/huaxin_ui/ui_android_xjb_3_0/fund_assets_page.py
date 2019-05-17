# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_assets_structure_page

BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"


class FundAssetsPage(PageObject):
    def __init__(self, web_driver):
        super(FundAssetsPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('基金资产', self.get_text(self.page_title, 'find_element_by_id'))
        # self.assert_values('资产结构', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_fund_assets_details(self, fund_type):
        self.assert_values(fund_type + '基金总资产(元)', self.get_text('com.shhxzq.xjb:id/tv_title', 'find_element_by_id'))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='最新收益(元)']")))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='累计收益(元)']")))

        page = self
        return page

    @robot_log
    def back_to_fund_assets_structure_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.fund_assets_structure_page.FundAssetsStructurePage(self.web_driver)
        return page
