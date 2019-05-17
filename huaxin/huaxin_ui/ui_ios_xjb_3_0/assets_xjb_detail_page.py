# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_3_0.recharge_page import RechargePage
from huaxin_ui.ui_ios_xjb_3_0.withdraw_page import WithdrawPage

from huaxin_ui.ui_ios_xjb_3_0.xjb_trade_detail_page import XjbTradeDetailPage
import huaxin_ui.ui_ios_xjb_3_0.income_detail_page
import huaxin_ui.ui_ios_xjb_3_0.xjb_asset_in_transit_page
import huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_ios_xjb_3_0.holding_assets_description_page

WITHDRAW = "accId_UIAButton_取出"
RECHARGE = "accId_UIAButton_存入"
XJB_TRADE_DETAIL = "accId_UIAButton_UIBarButtonItemLocationRight"
INTEREST_PER_WAN = "accId_UIAStaticText_(万份收益(元))"
INTEREST_ACCUMULATED = "accId_UIAStaticText_(累计收益(元))"
VIEW_HISTORY = "accId_UIAStaticText_(查看历史)"
SEVEN_DAYS_ANNUAL_RATE_OF_RETURN = "accId_UIAStaticText_(查看历史)"
ASSET_IN_TRANSIT = "xpathIOS_UIAStaticText_//UIAStaticText[contains(@label, '在途资产正在处理中')]"
XJB_PRODUCT_DETAIL = "accId_UIAStaticText_查看产品详情"
SWIPE_STOP = "swipe_accId_(UIButton_7日)"
PROFIT_HOME = "accId_UIAButton_(UIButton_%s)"
QUESTION_MARK = "accId_UIAButton_(UIButton_icon_questionAbout)"
current_page = []


class AssetsXjbDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsXjbDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_xjb_detail_page(self):
        self.assert_values('现金宝', self.get_text("//UIAStaticText[@label='现金宝']"))

        page = self

        return page

    @robot_log
    def go_to_xjb_description(self):
        self.perform_actions(QUESTION_MARK)

        page = huaxin_ui.ui_ios_xjb_3_0.holding_assets_description_page.HoldingAssetsDescriptionPage(self.web_driver)
        return page

    @robot_log
    def go_to_recharge_page(self):
        self.perform_actions(RECHARGE)
        page = RechargePage(self.web_driver)
        return page

    @robot_log
    def go_to_withdraw_page(self):
        self.perform_actions(WITHDRAW)
        page = WithdrawPage(self.web_driver)
        return page

    @robot_log
    def go_to_xjb_trade_detail_page(self):
        self.perform_actions(XJB_TRADE_DETAIL)
        page = XjbTradeDetailPage(self.web_driver)
        return page

    @robot_log
    def go_to_interest_page_per_wan(self):
        self.perform_actions(INTEREST_PER_WAN)
        page = huaxin_ui.ui_ios_xjb_3_0.income_detail_page.IncomeDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_interest_page_accumulated(self):
        self.perform_actions(INTEREST_ACCUMULATED)
        page = huaxin_ui.ui_ios_xjb_3_0.income_detail_page.IncomeDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_seven_days_annual_rate_of_return_page(self):
        self.perform_actions(SEVEN_DAYS_ANNUAL_RATE_OF_RETURN)
        page = huaxin_ui.ui_ios_xjb_3_0.income_detail_page.IncomeDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_asset_in_transit_page(self):
        self.perform_actions(
            ASSET_IN_TRANSIT
        )

        page = huaxin_ui.ui_ios_xjb_3_0.xjb_asset_in_transit_page.XjbAssetInTransitPage(self.web_driver)

        return page

    @robot_log
    def go_to_xjb_product_detail_page(self):
        self.perform_actions(
            XJB_PRODUCT_DETAIL
        )

        page = huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)

        return page

    @robot_log
    def view_xjb_seven_days_annual_rate_of_return(self, term):
        self.perform_actions("swipe_accId_//", SWIPE_STOP, 'U')
        self.perform_actions(PROFIT_HOME % term)
        page = self

        return page
