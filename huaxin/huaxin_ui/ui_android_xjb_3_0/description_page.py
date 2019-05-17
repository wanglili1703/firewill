# coding: utf-8
from _common.xjb_decorator import robot_log
from _common.page_object import PageObject
import huaxin_ui.ui_android_xjb_3_0.assets_xjb_detail_page
import huaxin_ui.ui_android_xjb_3_0.assets_high_end_detail_page
import huaxin_ui.ui_android_xjb_3_0.assets_fund_detail_page
import huaxin_ui.ui_android_xjb_3_0.assets_dqb_detail_page

BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"


class DescriptionPage(PageObject):
    def __init__(self, web_driver):
        super(DescriptionPage, self).__init__(web_driver)

        self._return_page = {
            'AssetsHighEndDetailPage': huaxin_ui.ui_android_xjb_3_0.assets_high_end_detail_page.AssetsHighEndDetailPage(
                self.web_driver),
            'AssetsXjbDetailPage': huaxin_ui.ui_android_xjb_3_0.assets_xjb_detail_page.AssetsXjbDetailPage(
                self.web_driver),
            'AssetsFundDetailPage': huaxin_ui.ui_android_xjb_3_0.assets_fund_detail_page.AssetsFundDetailPage(
                self.web_driver),
            'AssetsDqbDetailPage': huaxin_ui.ui_android_xjb_3_0.assets_dqb_detail_page.AssetsDqbDetailPage(
                self.web_driver),
        }

    @robot_log
    def verify_page_title(self):
        self.assert_values('说明', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_description(self, type=None):
        if type == 'xjb':
            self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='现金宝资产：']")))
            self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='昨日盈亏：']")))
            self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='累计盈亏：']")))
        elif type == 'dhb':
            self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='定期理财：']")))
        elif type == 'fund':
            self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='基金总资产：']")))
            self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='最新收益：']")))
            self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='累计收益：']")))
        elif type == 'vip':
            self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='高端理财总资产：']")))
            self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='高端理财累计收益：']")))

        page = self
        return page

    @robot_log
    def back_to_assets_xjb_detail_page(self, return_page):
        self.perform_actions(BACK)

        page = self._return_page[return_page]
        return page
