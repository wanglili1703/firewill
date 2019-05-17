# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_android_xjb_3_0.redeem_detail_page
import huaxin_ui.ui_android_xjb_3_0.trade_detail_page
import huaxin_ui.ui_android_xjb_3_0.select_convert_to_fund_page
import huaxin_ui.ui_android_xjb_3_0.expiry_processing_type_page
from _common.global_config import ASSERT_DICT

HOLDING_AMOUNT = "//android.widget.TextView[@text='持有金额(元)']/../following-sibling::android.widget.TextView[1]"
REDEEM = "xpath_//android.widget.Button[@text='卖出']"
RECORD = "xpath_//android.widget.TextView[@text='交易记录']"
DIVIDEND_TYPE = "xpath_//android.widget.TextView[@text='分红方式']"
DIVIDEND_REINVESTMENT = "xpath_//android.widget.CheckedTextView[@text='%s']"
SWITCH_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
SWITCH_RESULT = "//android.widget.TextView[@text='分红方式']/../../following-sibling::android.widget.LinearLayout[1]/android.widget.TextView[1]"
TRANSFER = "xpath_//android.widget.Button[@text='转换']"
AVAILABLE_AMOUNT = "//android.widget.TextView[@text='可用份额(份)']/../../following-sibling::android.widget.LinearLayout[1]/android.widget.TextView"
SWIPE_BEGIN = "swipe_xpath_//"
DIVIDEND_TYPE_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='分红方式']"
EXPIRY_PROCESSING_TYPE = "//android.widget.TextView[contains(@text,'12月29日')]/../following-sibling::android.widget.LinearLayout[1]/android.widget.TextView"
EXPIRY_PROCESSING_TYPE_2 = "//android.widget.TextView[contains(@text,'12月30日')]/../following-sibling::android.widget.LinearLayout[1]/android.widget.TextView"
EXPIRY_PROCESSING_TYPE_3 = "//android.widget.TextView[contains(@text,'12月31日')]/../following-sibling::android.widget.LinearLayout[1]/android.widget.TextView"
EXPIRY_DATE = "//android.widget.TextView[contains(@text,'%s')]"
DISPOSE_TYPE_TEXT = "//android.widget.TextView[contains(@text,'%s')]/following-sibling::android.widget.LinearLayout[1]/android.widget.TextView"
DISPOSE_TYPE = "//android.widget.TextView[contains(@text,'%s')]/../following-sibling::android.widget.LinearLayout[1]/android.widget.TextView[@resource-id='com.shhxzq.xjb:id/content']"
DISPOSE_AMOUNT = "//android.widget.TextView[contains(@text,'%s')]/../following-sibling::android.widget.LinearLayout[1]/android.widget.TextView[@resource-id='com.shhxzq.xjb:id/contentfoot']"
TYPE = "xpath_//android.widget.TextView[@text='%s']"


class FundRedeemPage(PageObject):
    def __init__(self, web_driver):
        super(FundRedeemPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self, fund_product):
        self.assert_values(fund_product, self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_redeem_page_details(self, fund_product):
        self.assert_values(fund_product.split('(')[0],
                           self.get_text('com.shhxzq.xjb:id/tv_fund_details_nm', 'find_element_by_id'))
        self.assert_values(ASSERT_DICT['holding_amount'], self.get_text(HOLDING_AMOUNT))

        page = self

        return page

    @robot_log
    def go_to_redeem_detail_page(self):
        self.perform_actions(REDEEM)

        page = huaxin_ui.ui_android_xjb_3_0.redeem_detail_page.RedeemDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_trade_records_page(self):
        available_amount = float(filter(lambda ch: ch in '0123456789.', self.get_text(AVAILABLE_AMOUNT)))
        ASSERT_DICT.update({'available_amount': available_amount})
        self.perform_actions(RECORD)

        page = huaxin_ui.ui_android_xjb_3_0.trade_detail_page.TradeDetailPage(self.web_driver)

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
        available_amount = float(filter(lambda ch: ch in '0123456789.', self.get_text(AVAILABLE_AMOUNT)))
        ASSERT_DICT.update({'available_amount': available_amount})
        self.perform_actions(TRANSFER)

        page = huaxin_ui.ui_android_xjb_3_0.select_convert_to_fund_page.SelectConvertToFundPage(self.web_driver)

        return page

    @robot_log
    def verify_available_amount(self):
        available_amount = float(filter(lambda ch: ch in '0123456789.', self.get_text(AVAILABLE_AMOUNT)))
        self.assert_values(ASSERT_DICT['available_amount'], available_amount)

        page = self
        return page

    @robot_log
    def verify_expiry_processing_type_details(self, processing_type, expiry_date):
        self.perform_actions(SWIPE_BEGIN, DIVIDEND_TYPE_SWIPE_STOP, 'U')
        self.assert_values('12月29日  到期', self.get_text(EXPIRY_DATE % expiry_date))
        self.assert_values('到期处理方式', self.get_text(DISPOSE_TYPE_TEXT % expiry_date))
        self.assert_values(processing_type, self.get_text(DISPOSE_TYPE % expiry_date))
        self.assert_values('到期份额(份):1,000,000.00', self.get_text(DISPOSE_AMOUNT % expiry_date))

        page = self
        return page

    @robot_log
    def go_to_expiry_processing_type_page(self, processing_type):
        self.perform_actions(SWIPE_BEGIN, DIVIDEND_TYPE_SWIPE_STOP, 'U')

        self.perform_actions(TYPE % processing_type)

        page = huaxin_ui.ui_android_xjb_3_0.expiry_processing_type_page.ExpiryProcessingTypePage(self.web_driver)
        return page
