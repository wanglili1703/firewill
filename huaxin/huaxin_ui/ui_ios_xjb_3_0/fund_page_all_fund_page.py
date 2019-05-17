# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.assets_page
import huaxin_ui.ui_ios_xjb_3_0.assets_fund_detail_page
import huaxin_ui.ui_ios_xjb_3_0.fund_product_search_page

FUND_PRODUCT_TYPE_ALL = "accId_UIAButton_(UIButton_全部)"
FUND_PRODUCT_TYPE_MIXED = "accId_UIAButton_(UIButton_混合型)"
FUND_PRODUCT_TYPE_STOCK = "accId_UIAButton_(UIButton_股票型)"
FUND_PRODUCT_TYPE_MONETARY = "accId_UIAButton_(UIButton_货币型)"
FUND_PRODUCT_TYPE_BOND = "accId_UIAButton_(UIButton_债券型)"
FUND_PRODUCT_TYPE_QDII = "accId_UIAButton_(UIButton_QDII)"
FUND_PRODUCT_TYPE_OTHER = "accId_UIAButton_(UIButton_其他)[POP]"
BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"
I_KNOW = "accId_UIAButton_(UIButton_我知道了)[POP]"
FUND_PRODUCT_SEARCH = "axis_IOS_基金代码/简拼/重仓资产"
current_page = []


class FundPageAllFundPage(PageObject):
    def __init__(self, web_driver):
        super(FundPageAllFundPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_all_fund_page(self):
        self.assert_values('基金名称', self.get_text("(基金名称)", "find_element_by_accessibility_id"))

    @robot_log
    def back_to_assets_page(self):
        self.perform_actions(BACK,
                             BACK,
                             BACK)

        page = huaxin_ui.ui_ios_xjb_3_0.assets_page.AssetsPage(self.web_driver)

        return page

    @robot_log
    def go_to_assets_fund_detail_page(self):
        self.perform_actions(BACK)
        page = huaxin_ui.ui_ios_xjb_3_0.assets_fund_detail_page.AssetsFundDetailPage(self.web_driver)

        return page

    @robot_log
    def close_tips(self):
        self.perform_actions(I_KNOW)
        page = self

        return page

    @robot_log
    def switch_to_other_fund_type_list(self):
        self.perform_actions(
            FUND_PRODUCT_TYPE_ALL,
            FUND_PRODUCT_TYPE_STOCK,
            FUND_PRODUCT_TYPE_MIXED,
            FUND_PRODUCT_TYPE_BOND,
            FUND_PRODUCT_TYPE_MONETARY,
            FUND_PRODUCT_TYPE_QDII,
            FUND_PRODUCT_TYPE_OTHER,
        )

    @robot_log
    def go_to_fund_product_search_page(self):
        self.perform_actions(FUND_PRODUCT_SEARCH)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_product_search_page.FundProductSearchPage(self.web_driver)

        return page
