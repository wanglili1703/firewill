# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

DIVIDENDS = "accId_UIAStaticText_分红拆分"

current_page = []


class FundNavPage(PageObject):
    def __init__(self, web_driver):
        super(FundNavPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_fund_nav_page(self, title):
        self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, '%s')]" % title))

        page = self
        return page

    @robot_log
    def verify_at_monetary_fund_history_nav_page(self, product_name):
        self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label,'%s')]" % product_name))
        self.assert_values("七日年化收益率", self.get_text("//UIAStaticText[@label='七日年化收益率']"))
        self.assert_values("日每万份收益(元)", self.get_text("//UIAStaticText[@label='日每万份收益(元)']"))

        page = self
        return page

    @robot_log
    def switch_to_dividends_split(self):
        self.perform_actions(DIVIDENDS)
        self.assert_values("分红详情", self.get_text("//UIAStaticText[@label='分红详情']"))
        self.assert_values("拆分详情", self.get_text("//UIAStaticText[@label='拆分详情']"))

    # 股权型高端产品
    @robot_log
    def high_end_history_nav_page(self):
        self.assert_values("日期", self.get_text("//UIAStaticText[@label='日期']"))
        self.assert_values("单位净值", self.get_text("//UIAStaticText[@label='单位净值']"))
        self.assert_values("累计净值", self.get_text("//UIAStaticText[@label='累计净值']"))
        self.assert_values("日涨跌幅", self.get_text("//UIAStaticText[@label='日涨跌幅']"))

    # 非货币型基金
    @robot_log
    def non_monetary_fund_history_nav_page(self):
        self.assert_values("日期", self.get_text("//UIAStaticText[@label='日期']"))
        self.assert_values("单位净值", self.get_text("//UIAStaticText[@label='单位净值']"))
        self.assert_values("累计净值", self.get_text("//UIAStaticText[@label='累计净值']"))
        self.assert_values("日涨幅", self.get_text("//UIAStaticText[@label='日涨幅']"))

    # 现金管理系列产品
    @robot_log
    def verify_at_vip_history_income(self):
        self.assert_values("七日年化收益率", self.get_text("//UIAStaticText[@label='七日年化收益率']"))
        self.assert_values("万份收益", self.get_text("//UIAStaticText[@label='万份收益']"))
        self.assert_values("历史收益", self.get_text("//UIAStaticText[@label='历史收益']"))
