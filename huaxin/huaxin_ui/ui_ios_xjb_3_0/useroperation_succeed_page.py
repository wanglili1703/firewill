# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.assets_high_end_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_page
import huaxin_ui.ui_ios_xjb_3_0.bank_card_management_page
import huaxin_ui.ui_ios_xjb_3_0.home_page
import huaxin_ui.ui_ios_xjb_3_0.assets_xjb_detail_page
import huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_ios_xjb_3_0.fund_plan_detail_page
import huaxin_ui.ui_ios_xjb_3_0.fund_plan_page

USER_OPERATION_COMPLETE = "accId_UIAButton_(UIButton_确认)"


class UserOperationSucceedPage(PageObject):
    def __init__(self, web_driver):
        super(UserOperationSucceedPage, self).__init__(web_driver)

        self._return_page = {
            'AssetsHighEndDetailPage': huaxin_ui.ui_ios_xjb_3_0.assets_high_end_detail_page.AssetsHighEndDetailPage(
                self.web_driver),
            'BankCardManagementPage': huaxin_ui.ui_ios_xjb_3_0.bank_card_management_page.BankCardManagementPage(
                self.web_driver),
            'FundPageFundDetail': huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(
                self.web_driver),
            'FundPlanPage': huaxin_ui.ui_ios_xjb_3_0.fund_plan_page.FundPlanPage(self.web_driver),
            'FundPlanDetailPage': huaxin_ui.ui_ios_xjb_3_0.fund_plan_detail_page.FundPlanDetailPage(
                self.web_driver),
            'AssetsXjbDetailPage': huaxin_ui.ui_ios_xjb_3_0.assets_xjb_detail_page.AssetsXjbDetailPage(
                self.web_driver),
            'HomePage': huaxin_ui.ui_ios_xjb_3_0.home_page.HomePage(self.web_driver),
            'AssetsPage': huaxin_ui.ui_ios_xjb_3_0.assets_page.AssetsPage(self.web_driver),
        }

    @robot_log
    def verify_page_title(self):
        self.assert_values('完成', self.get_text('//UIAStaticText[@label=\'完成\']'))
        page = self

        return page

    @robot_log
    def user_operation_complete(self, return_page=None):
        self.perform_actions(USER_OPERATION_COMPLETE)

        page = self._return_page[return_page]

        return page
