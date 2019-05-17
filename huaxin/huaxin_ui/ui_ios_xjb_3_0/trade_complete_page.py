# coding=utf-8
import time

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_ios_xjb_3_0.assets_page
import huaxin_ui.ui_ios_xjb_3_0.home_page
import huaxin_ui.ui_ios_xjb_3_0.assets_fund_detail_page
import huaxin_ui.ui_ios_xjb_3_0.pledge_page
import huaxin_ui.ui_ios_xjb_3_0.deposit_salary_page
import huaxin_ui.ui_ios_xjb_3_0.salary_financing_plan_detail_page
import huaxin_ui.ui_ios_xjb_3_0.repay_loan_page
import huaxin_ui.ui_ios_xjb_3_0.repay_loan_plan_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_fund_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_high_end_detail_page
import huaxin_ui.ui_ios_xjb_3_0.finance_high_end_page
import huaxin_ui.ui_ios_xjb_3_0.product_detail_page
import huaxin_ui.ui_ios_xjb_3_0.finance_dqb_page
import huaxin_ui.ui_ios_xjb_3_0.fund_product_search_page
import huaxin_ui.ui_ios_xjb_3_0.fund_holding_detail_page

TITLE_ELE = "//UIAStaticText[@label='完成']"
SUCCESS_BUTTON = "accId_UIAButton_(UIButton_确认)"
CANCEL = "accId_UIACollectionCell_取消[POP]"
current_page = []


class TradeCompletePage(PageObject):
    def __init__(self, web_driver):
        super(TradeCompletePage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
            "PledgePage": huaxin_ui.ui_ios_xjb_3_0.pledge_page.PledgePage(self.web_driver),
            "HomePage": huaxin_ui.ui_ios_xjb_3_0.home_page.HomePage(self.web_driver),
            "AssetsFundDetailPage": huaxin_ui.ui_ios_xjb_3_0.assets_fund_detail_page.AssetsFundDetailPage(
                self.web_driver),
            "AssetsHighEndDetailPage": huaxin_ui.ui_ios_xjb_3_0.assets_high_end_detail_page.AssetsHighEndDetailPage(
                self.web_driver),
            "DepositSalaryPage": huaxin_ui.ui_ios_xjb_3_0.deposit_salary_page.DepositSalaryPage(self.web_driver),
            "RepayLoanPage": huaxin_ui.ui_ios_xjb_3_0.repay_loan_page.RepayLoanPage(self.web_driver),
            "RepayLoanPlanDetailPage": huaxin_ui.ui_ios_xjb_3_0.repay_loan_plan_detail_page.RepayLoanPlanDetailPage(
                self.web_driver),
            "SalaryFinancingPlanDetailPage": huaxin_ui.ui_ios_xjb_3_0.salary_financing_plan_detail_page.SalaryFinancingPlanDetailPage(
                self.web_driver),
            "FinanceHighEndPage": huaxin_ui.ui_ios_xjb_3_0.finance_high_end_page.FinanceHighEndPage(self.web_driver),
            "ProductDetailPage": huaxin_ui.ui_ios_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver),
            "FinanceDqbPage": huaxin_ui.ui_ios_xjb_3_0.finance_dqb_page.FinanceDqbPage(self.web_driver),
            "FundProductSearchPage": huaxin_ui.ui_ios_xjb_3_0.fund_product_search_page.FundProductSearchPage(
                self.web_driver),
            "FundHoldingDetailPage": huaxin_ui.ui_ios_xjb_3_0.fund_holding_detail_page.FundHoldingDetailPage(
                self.web_driver)

        }

    @robot_log
    def confirm(self):
        self.verify_trade_complete_page_title()
        self.perform_actions(CANCEL,
                             SUCCESS_BUTTON)

    @robot_log
    def confirm_trade(self, return_page="HomePage"):
        self.confirm()
        page = self._return_page[return_page]

        return page

    @robot_log
    def confirm_fund_trade(self):
        self.confirm()
        page = huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)

        return page

    @robot_log
    def confirm_fund_redeem(self):
        self.confirm()
        page = huaxin_ui.ui_ios_xjb_3_0.assets_fund_detail_page.AssetsFundDetailPage(self.web_driver)

        return page

    @robot_log
    def confirm_trade_from_xjb_page(self):
        time.sleep(1)
        self.confirm()
        page = huaxin_ui.ui_ios_xjb_3_0.assets_page.AssetsPage(self.web_driver)

        return page

    @robot_log
    def verify_trade_complete_page_title(self):
        title = self.get_text(TITLE_ELE)
        self.assert_values('完成', title)
