# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page

AMOUNT = "xpathIOS_UIATextField_IOS//UIATextField"
FUND_CONVERT_CONFIRM = "accId_UIAButton_(UIButton_确定)"
TRADE_PASSWORD = "xpathIOS_UIATextField_//UIAStaticText[@label='请输入交易密码']/following-sibling::UIATextField"


class FundConvertPage(PageObject):
    def __init__(self, web_driver):
        super(FundConvertPage, self).__init__(web_driver)

    @robot_log
    def verify_at_fund_convert_page(self):
        self.assert_values('转换', self.get_text("//UIAStaticText[@label='转换']"))

        page = self
        return page

    @robot_log
    def verify_fund_convert_details(self, fund_convert_from, fund_convert_to):
        self.assert_values(True,
                           self.element_exist("//UIAStaticText[contains(@label,'%s')]" % fund_convert_from))
        self.assert_values(True,
                           self.element_exist("//UIAStaticText[contains(@label,'%s')]" % fund_convert_to))
        self.assert_values('极速转换', self.get_text('(极速转换)', 'find_element_by_accessibility_id'))
        self.assert_values(fund_convert_to,
                           self.get_text('//UIAStaticText[@label=\'转入基金\']/following-sibling::UIAStaticText'))
        self.assert_values(fund_convert_from,
                           self.get_text('//UIAStaticText[@label=\'转出基金\']/following-sibling::UIAStaticText'))
        self.assert_values(True,
                           self.element_exist("//UIAStaticText[@label='持有份额(份)']"))
        self.assert_values(True,
                           self.element_exist("//UIAStaticText[@label='可转出份额(份)']"))

        page = self
        return page

    @robot_log
    def fund_convert(self, amount, trade_password):
        available = float(filter(lambda ch: ch in '0123456789.',
                                 self.get_text(
                                     '//UIAStaticText[@label=\'可转出份额(份)\']/following-sibling::UIAStaticText')).replace(',', ''))
        self.perform_actions(AMOUNT, amount,
                             FUND_CONVERT_CONFIRM,
                             TRADE_PASSWORD, trade_password,
                             )

        available_amount = available - float(amount)
        ASSERT_DICT.update({'available_amount': available_amount})
        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page
