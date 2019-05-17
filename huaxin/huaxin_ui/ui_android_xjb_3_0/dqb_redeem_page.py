# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.redeem_detail_page
import huaxin_ui.ui_android_xjb_3_0.trade_detail_page

REDEEM = "xpath_//android.widget.Button[@text='取回']"
RECORD = "xpath_//android.widget.TextView[@text='交易记录']"
SWIPE_BEGIN = "swipe_xpath_//"
RECORD_STOP = "swipe_xpath_//android.widget.TextView[@text='交易记录']"


class DqbRedeemPage(PageObject):
    def __init__(self, web_driver):
        super(DqbRedeemPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self, product_name):
        self.assert_values(product_name, self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_redeem_detail_page(self):
        self.perform_actions(REDEEM)

        page = huaxin_ui.ui_android_xjb_3_0.redeem_detail_page.RedeemDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_trade_records_page(self):
        self.perform_actions(
            SWIPE_BEGIN, RECORD_STOP, 'U',
            RECORD
        )

        page = huaxin_ui.ui_android_xjb_3_0.trade_detail_page.TradeDetailPage(self.web_driver)

        return page
