# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.assets_dqb_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_high_end_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_fund_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_xjb_detail_page

BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"
current_page = []


class HoldingAssetsDescriptionPage(PageObject):
    def __init__(self, web_driver):
        super(HoldingAssetsDescriptionPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
            "AssetsDqbDetailPage": huaxin_ui.ui_ios_xjb_3_0.assets_dqb_detail_page.AssetsDqbDetailPage(self.web_driver),
            "AssetsFundDetailPage": huaxin_ui.ui_ios_xjb_3_0.assets_fund_detail_page.AssetsFundDetailPage(
                self.web_driver),
            "AssetsHighEndDetailPage": huaxin_ui.ui_ios_xjb_3_0.assets_high_end_detail_page.AssetsHighEndDetailPage(
                self.web_driver),
            "AssetsXjbDetailPage": huaxin_ui.ui_ios_xjb_3_0.assets_xjb_detail_page.AssetsXjbDetailPage(self.web_driver),
        }

    @robot_log
    def verify_description(self, description, return_page):
        self.assert_values(True, self.element_exist("说明", "find_element_by_accessibility_id"))
        self.assert_values(True, self.element_exist("//UIAStaticText[@label='%s']" % description))

        self.perform_actions(BACK)
        page = self._return_page[return_page]

        return page
