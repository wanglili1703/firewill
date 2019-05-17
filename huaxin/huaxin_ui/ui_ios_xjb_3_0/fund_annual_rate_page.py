# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.product_detail_page

DIVIDENDS = "accId_UIAStaticText_分红拆分"
BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"
current_page = []


# 货币基金历史年化收益页面
class FundAnnualRatePage(PageObject):
    def __init__(self, web_driver):
        super(FundAnnualRatePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_fund_annual_rate_page(self, product_name):
        self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label,'%s')]" % product_name))
        self.assert_values("七日年化收益率", self.get_text("//UIAStaticText[@label='七日年化收益率']"))
        self.assert_values("日每万份收益(元)", self.get_text("//UIAStaticText[@label='日每万份收益(元)']"))

        page = self
        return page

    @robot_log
    def back_to_previous_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_ios_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)
        return page

    @robot_log
    def verify_at_vip_history_income(self):
        self.assert_values("七日年化收益率", self.get_text("//UIAStaticText[@label='七日年化收益率']"))
        self.assert_values("万份收益", self.get_text("//UIAStaticText[@label='万份收益']"))
        self.assert_values("历史收益", self.get_text("//UIAStaticText[@label='历史收益']"))
