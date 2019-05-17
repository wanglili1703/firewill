# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

import huaxin_ui.ui_android_xjb_3_0.fund_assets_page
import time

FUND_TYPE = "xpath_//android.view.View[contains(@content-desc,'%s') and @focusable='true']"


class FundAssetsStructurePage(PageObject):
    def __init__(self, web_driver):
        super(FundAssetsStructurePage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('资产结构', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_fund_assets_structure_details(self):
        self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='资产配置']")))
        self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='混合型']")))
        self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='货币型']")))
        self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='行业分布']")))
        self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='债券品种']")))

        page = self
        return page

    @robot_log
    def go_to_fund_assets_page(self, fund_type):
        time.sleep(2)
        self.perform_actions(
            FUND_TYPE % (fund_type)
        )

        page = huaxin_ui.ui_android_xjb_3_0.fund_assets_page.FundAssetsPage(self.web_driver)

        return page
