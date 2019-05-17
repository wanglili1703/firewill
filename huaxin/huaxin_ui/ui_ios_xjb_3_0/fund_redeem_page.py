# coding: utf-8
from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.expiry_processing_type_page
import huaxin_ui.ui_ios_xjb_3_0.select_convert_to_fund_page

REDEEM = "xpath_//android.widget.Button[@text='卖出']"
HOLDING_AMOUNT = ""
DIVIDEND_TYPE = ""
DIVIDEND_REINVESTMENT = ""
SWITCH_CONFIRM = ""
SWITCH_RESULT = ""
TRANSFER = "accId_UIAButton_(UIButton_转换)"
AVAILABLE_AMOUNT = ""
DIVIDEND_TYPE_SWIPE_STOP= ""
EXPIRY_DATE = ""
DISPOSE_TYPE_TEXT = ""
DISPOSE_TYPE = ""
DISPOSE_AMOUNT = ""
TYPE = ""


class FundRedeemPage(PageObject):
    def __init__(self, web_driver):
        super(FundRedeemPage, self).__init__(web_driver)

    @robot_log
    def verify_at_fund_redeem_page(self, fund_product):
        self.assert_values(fund_product, self.get_text("//UIAStaticText[@label='%s']") % fund_product)

        page = self
        return page

    @robot_log
    def verify_redeem_page_details(self, fund_product):
        self.assert_values(fund_product.split('(')[0], self.get_text(""))
        self.assert_values(ASSERT_DICT['holding_amount'], self.get_text(HOLDING_AMOUNT))

        page = self
        return page

    @robot_log
    def fund_dividend_type_switch(self, dividend_type):
        self.perform_actions(DIVIDEND_TYPE)
        self.perform_actions(DIVIDEND_REINVESTMENT % dividend_type)
        self.perform_actions(SWITCH_CONFIRM)
        self.assert_values(dividend_type, self.get_text(SWITCH_RESULT))

        page = self
        return page

    @robot_log
    def go_to_select_convert_to_fund_page(self):
        self.perform_actions(TRANSFER)

        page = huaxin_ui.ui_ios_xjb_3_0.select_convert_to_fund_page.SelectConvertToFundPage(self.web_driver)
        return page

    @robot_log
    def verify_available_amount(self):
        available_amount = float(filter(lambda ch: ch in '0123456789.', self.get_text(AVAILABLE_AMOUNT)))
        self.assert_values(ASSERT_DICT['available_amount'], available_amount)

        page = self
        return page

    @robot_log
    def verify_expiry_processing_type_details(self, processing_type, expiry_date):
        self.perform_actions("swipe_accId_//", DIVIDEND_TYPE_SWIPE_STOP, 'U')
        self.assert_values('12月29日  到期', self.get_text(EXPIRY_DATE % expiry_date))
        self.assert_values('到期处理方式', self.get_text(DISPOSE_TYPE_TEXT % expiry_date))
        self.assert_values(processing_type, self.get_text(DISPOSE_TYPE % expiry_date))
        self.assert_values('到期份额(份):1,000,000.00', self.get_text(DISPOSE_AMOUNT % expiry_date))

        page = self
        return page

    @robot_log
    def go_to_expiry_processing_type_page(self, processing_type):
        self.perform_actions("swipe_accId_//", DIVIDEND_TYPE_SWIPE_STOP, 'U')

        self.perform_actions(TYPE % processing_type)

        page = huaxin_ui.ui_ios_xjb_3_0.expiry_processing_type_page.ExpiryProcessingTypePage(self.web_driver)
        return page
