# coding: utf-8
from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.product_purchase_page
import huaxin_ui.ui_ios_xjb_3_0.product_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_fund_detail_page
import huaxin_ui.ui_ios_xjb_3_0.expiry_processing_type_page
import huaxin_ui.ui_ios_xjb_3_0.select_convert_to_fund_page
import huaxin_ui.ui_ios_xjb_3_0.trade_detail_page

SOLD_OUT = "accId_UIAButton_卖出"
PRODUCT_DETAIL = "accId_UIAStaticTex_查看产品详情"
SUPPLEMENTARY_PURCHASE = "accId_UIAButton_继续买入"
BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"

RECORD = "accId_UIAStaticText_交易记录"
HOLDING_AMOUNT = "//UIAStaticText[@label=\'持有份额(份)\']/following-sibling::UIAStaticText"
DIVIDEND_TYPE = "accId_UIAStaticText_分红方式"
DIVIDEND_KINDS = "accId_UIAStaticText_%s"
SWITCH_CONFIRM = "accId_UIAButton_确定"
SWITCH_RESULT = "//UIAStaticText[@label='分红方式']/following-sibling::UIAStaticText"
TRANSFER = "accId_UIAButton_(UIButton_转换)"
AVAILABLE_AMOUNT = "//UIAStaticText[@label=\'可用份额(份)\']/following-sibling::UIAStaticText"
DIVIDEND_TYPE_SWIPE_STOP = ""
EXPIRY_DATE = ""
DISPOSE_TYPE_TEXT = ""
DISPOSE_TYPE = ""
DISPOSE_AMOUNT = ""
TYPE = ""
BUY_CONTINUE = "accId_UIAButton_继续买入"


class FundHoldingDetailPage(PageObject):
    def __init__(self, web_driver):
        super(FundHoldingDetailPage, self).__init__(web_driver)

        self._return_page = {
            "AssetsFundDetailPage": huaxin_ui.ui_ios_xjb_3_0.assets_fund_detail_page.AssetsFundDetailPage(
                self.web_driver),
        }

    @robot_log
    def verify_at_fund_holding_detail_page(self, product_name):
        self.assert_values("持有详情", self.get_text("//UIAStaticText[@label='持有详情']"))
        if str(product_name).__contains__('('):
            product_name = str(product_name).split('(')[0]
        self.assert_values(product_name, self.get_text('(%s)' % product_name, 'find_element_by_accessibility_id'))

        page = self
        return page

    @robot_log
    def back_to_previous_page(self, return_page):
        self.perform_actions(BACK)

        page = self._return_page[return_page]
        return page

    @robot_log
    def go_to_product_detail_page(self):
        self.perform_actions(
            PRODUCT_DETAIL
        )

        page = huaxin_ui.ui_ios_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)
        return page

    @robot_log
    def fund_product_supplementary_purchase(self):
        self.perform_actions(
            SUPPLEMENTARY_PURCHASE
        )

        if self.element_exist(u'风险提示', 'find_element_by_accessibility_id'):
            self.perform_actions(
                BUY_CONTINUE,
            )

        page = huaxin_ui.ui_ios_xjb_3_0.product_purchase_page.ProductPurchasePage(self.web_driver)
        return page

    @robot_log
    def verify_holding_page_details(self, fund_product):
        self.assert_values(fund_product.split('(')[0], self.get_text(""))
        self.assert_values(ASSERT_DICT['holding_amount'], self.get_text(HOLDING_AMOUNT))

        page = self
        return page

    @robot_log
    def fund_dividend_type_switch(self, dividend_type):
        self.perform_actions(DIVIDEND_TYPE)
        self.perform_actions(DIVIDEND_KINDS % dividend_type)
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

    @robot_log
    def go_to_trade_records_page(self):
        available_amount = float(filter(lambda ch: ch in '0123456789.', self.get_text(AVAILABLE_AMOUNT)))
        ASSERT_DICT.update({'available_amount': available_amount})
        self.perform_actions(RECORD)

        page = huaxin_ui.ui_ios_xjb_3_0.trade_detail_page.TradeDetailPage(self.web_driver)

        return page
