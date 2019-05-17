# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.assets_high_end_detail_page
import huaxin_ui.ui_android_xjb_3_0.assets_page
import huaxin_ui.ui_android_xjb_3_0.bank_card_management_page
import huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_android_xjb_3_0.fund_plan_detail_page
import huaxin_ui.ui_android_xjb_3_0.assets_xjb_detail_page
import huaxin_ui.ui_android_xjb_3_0.home_page
import huaxin_ui.ui_android_xjb_3_0.assets_fund_detail_page
import huaxin_ui.ui_android_xjb_3_0.pledge_page
import huaxin_ui.ui_android_xjb_3_0.add_credit_card_page
import huaxin_ui.ui_android_xjb_3_0.credit_card_repay_page
import huaxin_ui.ui_android_xjb_3_0.fund_product_search_page
import huaxin_ui.ui_android_xjb_3_0.security_center_page
import huaxin_ui.ui_android_xjb_3_0.finance_high_end_page
import huaxin_ui.ui_android_xjb_3_0.finance_dqb_page
import huaxin_ui.ui_android_xjb_3_0.assets_dqb_detail_page
import huaxin_ui.ui_android_xjb_3_0.fund_redeem_page
import huaxin_ui.ui_android_xjb_3_0.recharge_page
import huaxin_ui.ui_android_xjb_3_0.login_page
import huaxin_ui.ui_android_xjb_3_0.personal_setting_page

PERMISSION_CLOSE="xpath_//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button'][POP]"
USER_OPERATION_COMPLETE = "xpath_//android.widget.Button[@text='确认']"


class UserOperationSucceedPage(PageObject):
    def __init__(self, web_driver):
        super(UserOperationSucceedPage, self).__init__(web_driver)

        self._return_page = {
            'AssetsHighEndDetailPage': huaxin_ui.ui_android_xjb_3_0.assets_high_end_detail_page.AssetsHighEndDetailPage(self.web_driver),
            'AssetsDqbDetailPage': huaxin_ui.ui_android_xjb_3_0.assets_dqb_detail_page.AssetsDqbDetailPage(self.web_driver),
            'BankCardManagementPage': huaxin_ui.ui_android_xjb_3_0.bank_card_management_page.BankCardManagementPage(self.web_driver),
            'FundPageFundDetail': huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver),
            'FundPlanDetailPage': huaxin_ui.ui_android_xjb_3_0.fund_plan_detail_page.FundPlanDetailPage(self.web_driver),
            'AssetsXjbDetailPage': huaxin_ui.ui_android_xjb_3_0.assets_xjb_detail_page.AssetsXjbDetailPage(self.web_driver),
            'HomePage': huaxin_ui.ui_android_xjb_3_0.home_page.HomePage(self.web_driver),
            'AssetsPage': huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver),
            'AssetsFundDetailPage': huaxin_ui.ui_android_xjb_3_0.assets_fund_detail_page.AssetsFundDetailPage(self.web_driver),
            'Pledge_page': huaxin_ui.ui_android_xjb_3_0.pledge_page.PledgePage(self.web_driver),
            'AddCreditCardPage': huaxin_ui.ui_android_xjb_3_0.add_credit_card_page.AddCreditCardPage(self.web_driver),
            'CreditCardRepayPage': huaxin_ui.ui_android_xjb_3_0.credit_card_repay_page.CreditCardRepayPage(self.web_driver),
            'FundProductSearchPage': huaxin_ui.ui_android_xjb_3_0.fund_product_search_page.FundProductSearchPage(self.web_driver),
            'SecurityCenterPage': huaxin_ui.ui_android_xjb_3_0.security_center_page.SecurityCenterPage(self.web_driver),
            'FinanceHighEndPage': huaxin_ui.ui_android_xjb_3_0.finance_high_end_page.FinanceHighEndPage(self.web_driver),
            'FinanceDqbPage': huaxin_ui.ui_android_xjb_3_0.finance_dqb_page.FinanceDqbPage(self.web_driver),
            'FundRedeemPage': huaxin_ui.ui_android_xjb_3_0.fund_redeem_page.FundRedeemPage(self.web_driver),
            'RechargePage': huaxin_ui.ui_android_xjb_3_0.recharge_page.RechargePage(self.web_driver),
            'LoginPage': huaxin_ui.ui_android_xjb_3_0.login_page.LoginPage(self.web_driver),
            'PersonalSettingPage': huaxin_ui.ui_android_xjb_3_0.personal_setting_page.PersonalSettingPage(self.web_driver),
        }

    @robot_log
    def verify_page_title(self):
        self.assert_values('完成', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))
        page = self

        return page

    @robot_log
    def user_operation_complete(self, return_page=None):
        self.perform_actions(USER_OPERATION_COMPLETE)

        page = self._return_page[return_page]
        self.perform_actions(PERMISSION_CLOSE)

        return page
