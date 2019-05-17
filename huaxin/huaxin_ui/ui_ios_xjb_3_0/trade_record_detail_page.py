# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from decimal import Decimal
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page

current_page = []
TRADE_TYPE_LIST = "xpathIOS_UIAButton_//UIAButton[@label='定活宝']"
TRADE_TYPE_DONE = "accId_UIAButton_完成"

TRADE_STATUS_LIST = "xpathIOS_UIAButton_//UIAButton[@label='全部状态']"
TRADE_STATUS_DONE = "accId_UIAButton_完成"

CANCEL_ORDER = "accId_UIAButton_UIBarButtonItemLocationRight"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"


class TradeRecordDetailPage(PageObject):
    def __init__(self, web_driver):
        super(TradeRecordDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_trade_record_detail_page(self):
        title = self.get_text("//UIAStaticText[@label='交易详情']")
        self.assert_values('交易详情', title)

    # product_type='2': 基金
    @robot_log
    def verify_trade_record_info(self, product_name, trade_type, status, amount=None, product_type=None):
        self.assert_values('%s-%s' % (trade_type, product_name),
                           self.get_text("(%s-%s)" % (trade_type, product_name), "find_element_by_accessibility_id"))
        self.assert_values(status, self.get_text("(%s)" % status, "find_element_by_accessibility_id"))
        if amount is not None:
            amount = Decimal(amount).quantize(Decimal("0.00"))
            if product_type is None:
                self.assert_values('¥%s' % str(format(amount, ',')),
                                   self.get_text("(¥%s)" % format(amount, ','), "find_element_by_accessibility_id"))
            else:
                self.assert_values('%s份' % str(format(amount, ',')),
                                   self.get_text("(%s份)" % format(amount, ','), "find_element_by_accessibility_id"))

        page = self
        return page

    @robot_log
    def cancel_order(self, trade_password):
        self.perform_actions(CANCEL_ORDER,
                             TRADE_PASSWORD, trade_password,
                             )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)
        return page
