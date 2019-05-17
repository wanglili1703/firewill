# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_assets_page

FUND_TYPE = "//UIALink[@label='%s']/following-sibling::UIALink"
FUND_TYPE_NAV = "xpathIOS_UIALink_%s" % FUND_TYPE


class FundAssetsStructurePage(PageObject):
    def __init__(self, web_driver):
        super(FundAssetsStructurePage, self).__init__(web_driver)

    @robot_log
    def verify_at_fund_assets_structure_page(self):
        self.assert_values('资产结构', self.get_text("//UIAStaticText[@label='资产结构']"))

        page = self
        return page

    @robot_log
    def verify_fund_assets_structure_details(self):
        self.assert_values(True, self.element_exist(FUND_TYPE % '混合型'))
        self.assert_values(True, self.element_exist(FUND_TYPE % "货币型"))
        self.assert_values(True, self.element_exist("//UIAStaticText[@label='行业分布']"))
        self.assert_values(True, self.element_exist("//UIAStaticText[@label='债券品种']"))

        page = self
        return page

    @robot_log
    def go_to_fund_assets_page(self, fund_type):
        self.perform_actions(
            FUND_TYPE_NAV % fund_type
        )

        page = huaxin_ui.ui_ios_xjb_3_0.fund_assets_page.FundAssetsPage(self.web_driver)

        return page
