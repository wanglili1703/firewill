# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_annual_rate_page
import huaxin_ui.ui_ios_xjb_3_0.fund_trade_detail_page

INTEREST_PER_WAN = "xpathIOS_UIAButton_//UIAButton[@label='万份收益']"
SEVEN_DAYS_RATE = "xpathIOS_UIAButton_//UIAButton[@label='七日年化收益率']"
MORE = "accId_UIAStaticText_(查看更多)"
VIEW_HISTORY = "accId_UIAStaticText_(UIButton_查看历史)"
TRADE_RECORD = "accId_UIAButton_(UIButton_交易记录)"
current_page = []


class HistoryHoldingVipDetailPage(PageObject):
    def __init__(self, web_driver):
        super(HistoryHoldingVipDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_history_vip_holding_detail(self, product_name):
        self.assert_values(product_name, self.get_text("//UIAStaticText[@label='%s']" % product_name))
        self.assert_values('累计收益(元)', self.get_text("//UIAStaticText[@label='累计收益(元)']"))
        self.assert_values('公告详情', self.get_text("//UIAStaticText[@label='公告详情']"))
        self.assert_values('开放说明', self.get_text("//UIAStaticText[@label='开放说明']"))
        self.assert_values('合同文件', self.get_text("//UIAStaticText[@label='合同文件']"))

    @robot_log
    def view_monetary_fund_annual_rate_info_by_clicking_more(self):
        self.perform_actions(INTEREST_PER_WAN,
                             MORE)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_annual_rate_page.FundAnnualRatePage(self.web_driver)
        return page

    @robot_log
    def view_monetary_fund_annual_rate_info_by_clicking_view_history(self):
        self.perform_actions(SEVEN_DAYS_RATE)
        self.assert_values(True, self.element_exist("//UIAButton[contains(@label, '同类货币基金')]"))
        self.perform_actions(VIEW_HISTORY)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_annual_rate_page.FundAnnualRatePage(self.web_driver)
        return page

    @robot_log
    def click_trade_record(self):
        self.perform_actions(TRADE_RECORD)

        title = self.get_text("//UIAStaticText[@label='交易记录']")
        self.assert_values('交易记录', title)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_trade_detail_page.FundTradeDetailPage(self.web_driver)
        return page
