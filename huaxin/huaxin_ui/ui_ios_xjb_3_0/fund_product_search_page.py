# coding: utf-8
import time

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_ios_xjb_3_0.fund_selected_page
import huaxin_ui.ui_ios_xjb_3_0.fund_convert_page
import huaxin_ui.ui_ios_xjb_3_0.select_convert_to_fund_page
from _tools.mysql_xjb_tools import MysqlXjbTools

FUND_PRODUCT_INPUT = "accId_UIASearchBar_基金代码/简拼/重仓资产"
FUND_PRODUCT_NAME = "xpathIOS_UIAStaticText_//UIATableCell[@name='(HXSearchOrAddFundTableViewCell)']/UIAStaticText[contains(@name, '%s')]"
FUND_PRODUCT_NM_CONVERT = "xpathIOS_UIAStaticText_//UIATableView[2]/UIATableCell[@name='(SearchTransitionFundCell)']/UIAStaticText[contains(@name, '%s')]"
BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"
CANCEL = "accId_UIAButton_(UIButton_取消)"
BUY_CONTINUE = "accId_UIAButton_继续买入[POP]"
MOBILE_CODE = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
VERIFY_CODE_CONFIRM = "accId_UIAButton_(UIButton_确认)"


class FundProductSearchPage(PageObject):
    def __init__(self, web_driver):
        super(FundProductSearchPage, self).__init__(web_driver)
        self._return_page = {
            "SelectConvertToFundPage": huaxin_ui.ui_ios_xjb_3_0.select_convert_to_fund_page.SelectConvertToFundPage(
                self.web_driver),
        }

    @robot_log
    def verify_page_title(self):
        self.assert_values('基金代码/简拼/重仓资产', self.get_text('基金代码/简拼/重仓资产', 'find_element_by_accessibility_id'))
        page = self

        return page

    @robot_log
    def search_fund_products(self, fund_product_name, operation_type=None, mobile=None):
        if operation_type is None:
            self.perform_actions(FUND_PRODUCT_INPUT, fund_product_name,
                                 FUND_PRODUCT_NAME % fund_product_name)
            page = huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)
        else:
            self.perform_actions(FUND_PRODUCT_INPUT, fund_product_name)
            self.perform_actions(FUND_PRODUCT_NM_CONVERT % fund_product_name)

            # 当出现购买产品风险高于用户的风险测评结果, 就会出现风险提示, 有些还需要验证码输入.
            if self.element_exist(u'风险提示', 'find_element_by_accessibility_id'):
                self.perform_actions(
                    BUY_CONTINUE,
                )

                if self.element_exist("(UIButton_确认)", "find_element_by_accessibility_id"):
                    verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile, template_id='as_risk_not_match')

                    self.perform_actions(
                        MOBILE_CODE, verify_code,
                        VERIFY_CODE_CONFIRM,
                    )

            page = huaxin_ui.ui_ios_xjb_3_0.fund_convert_page.FundConvertPage(self.web_driver)

        return page

    @robot_log
    def back_to_fund_selected_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_selected_page.FundSelectedPage(self.web_driver)
        return page

    @robot_log
    def cancel_search(self, return_page):
        self.perform_actions(CANCEL)

        page = self._return_page[return_page]
        return page
