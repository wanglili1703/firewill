# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.assets_xjb_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_high_end_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_fund_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_dqb_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_certification_preview_page

TOTAL_ASSETS = "//UIAStaticText[@name='总资产(元)']"
XJB = "//UIAStaticText[@name='现金宝']"
DHB = "//UIAStaticText[@name='定活宝']"
FUND = "//UIAStaticText[@name='金']"
VIP_PRODUCT = "//UIAStaticText[@name='端']"
DOWNLOAD = "下载资产证明"
TRADE_PASSWORD = "xpathIOS_UIATextField_//UIATextField"


class AssetsAnalysisPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsAnalysisPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('资产分析', self.get_text("//UIAStaticText[@label='资产分析']"))

        page = self
        return page

    @robot_log
    def verify_assets_items(self):
        self.assert_values(True, self.element_exist(TOTAL_ASSETS))
        self.assert_values(True, self.element_exist(XJB))

        page = self
        return page

    @robot_log
    def go_to_xjb_detail_page(self):
        self.perform_actions(
            "xpathIOS_UIAStaticText_%s" % XJB
        )

        page = huaxin_ui.ui_ios_xjb_3_0.assets_xjb_detail_page.AssetsXjbDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_assets_dhb_detail_page(self):
        self.perform_actions(
            "xpathIOS_UIAStaticText_%s" % DHB
        )

        page = huaxin_ui.ui_ios_xjb_3_0.assets_dqb_detail_page.AssetsDqbDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_assets_fund_detail_page(self):
        self.perform_actions(
            "xpathIOS_UIAStaticText_%s" % FUND
        )

        page = huaxin_ui.ui_ios_xjb_3_0.assets_fund_detail_page.AssetsFundDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_assets_high_end_detail_page(self):
        self.perform_actions(
            "xpathIOS_UIAStaticText_%s" % VIP_PRODUCT
        )

        page = huaxin_ui.ui_ios_xjb_3_0.assets_high_end_detail_page.AssetsHighEndDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_assets_certification_preview_page(self, trade_password):
        self.perform_actions(
            "accId_UIAStaticText_%s" % DOWNLOAD,
            TRADE_PASSWORD, trade_password,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.assets_certification_preview_page.AssetsCertificationPreviewPage(
            self.web_driver)

        return page
