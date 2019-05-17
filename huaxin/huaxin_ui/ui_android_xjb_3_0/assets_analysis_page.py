# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_android_xjb_3_0.assets_xjb_detail_page
import huaxin_ui.ui_android_xjb_3_0.assets_high_end_detail_page
import huaxin_ui.ui_android_xjb_3_0.assets_fund_detail_page
import huaxin_ui.ui_android_xjb_3_0.assets_dqb_detail_page
import huaxin_ui.ui_android_xjb_3_0.assets_certification_preview_page
import time

TOTAL_ASSETS = "xpath_//android.view.View[@content-desc='总资产(元)']"
XJB = "xpath_//android.view.View[@content-desc='现金宝']"
DHB = "xpath_//android.view.View[@content-desc='定活宝']"
FUND = "xpath_//android.view.View[@content-desc='基']"
VIPPRODUCT = "xpath_//android.view.View[@content-desc='高']"
DOWNLOAD = "xpath_//android.widget.Button[@text='下载资产证明']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
ALLOW = "xpath_//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button']"


class AssetsAnalysisPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsAnalysisPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        time.sleep(5)
        self.assert_values('资产分析', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_assets_items(self):
        self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='总资产(元)']")))
        self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='现金宝']")))
        self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='定活宝']")))
        self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='基']")))
        self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='高']")))
        total_assets = self.get_attribute(
            "//android.view.View[@content-desc='总资产(元)']/following-sibling::android.view.View")
        xjb_assets = self.get_attribute("//android.view.View[@content-desc='现金宝']/following-sibling::android.view.View")
        dhb_assets = self.get_attribute("//android.view.View[@content-desc='定活宝']/following-sibling::android.view.View")
        fund_assets = self.get_attribute("//android.view.View[@content-desc='基']/../following-sibling::android.view.View")
        vipproduct_assets = self.get_attribute(
            "//android.view.View[@content-desc='高']/../following-sibling::android.view.View")
        self.assert_values(ASSERT_DICT['total_asset'], total_assets.replace(',', ''))
        self.assert_values(ASSERT_DICT['xjb_total_assets_login'], xjb_assets.replace(',', ''))
        self.assert_values(ASSERT_DICT['dhb_asset_login'], dhb_assets.replace(',', ''))
        self.assert_values(ASSERT_DICT['fund_asset_login'], fund_assets.replace(',', ''))
        self.assert_values(ASSERT_DICT['vip_asset_login'], vipproduct_assets.replace(',', ''))

        page = self
        return page

    @robot_log
    def go_to_xjb_detail_page(self):
        self.perform_actions(
            XJB
        )

        page = huaxin_ui.ui_android_xjb_3_0.assets_xjb_detail_page.AssetsXjbDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_assets_dhb_detail_page(self):
        self.perform_actions(
            DHB
        )

        page = huaxin_ui.ui_android_xjb_3_0.assets_dqb_detail_page.AssetsDqbDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_assets_fund_detail_page(self):
        self.perform_actions(
            FUND
        )

        page = huaxin_ui.ui_android_xjb_3_0.assets_fund_detail_page.AssetsFundDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_assets_high_end_detail_page(self):
        self.perform_actions(
            VIPPRODUCT
        )

        page = huaxin_ui.ui_android_xjb_3_0.assets_high_end_detail_page.AssetsHighEndDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_assets_certification_preview_page(self, trade_password):
        self.perform_actions(
            DOWNLOAD,
            TRADE_PASSWORD, trade_password,
        )

        # self.perform_actions(ALLOW)

        page = huaxin_ui.ui_android_xjb_3_0.assets_certification_preview_page.AssetsCertificationPreviewPage(
            self.web_driver)

        return page
