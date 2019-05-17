# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT

current_page = []
TRADE_TYPE_LIST = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/title_actionbar']"
TRADE_TYPE_ALL = "xpath_//android.widget.CheckedTextView[@text='全部']"
TRADE_TYPE_RECHARGE = "xpath_//android.widget.CheckedTextView[@text='存入']"
TRADE_TYPE_WITHDRAW = "xpath_//android.widget.CheckedTextView[@text='取出']"
TRADE_TYPE_INCOME = "xpath_//android.widget.CheckedTextView[@text='收益']"
TRADE_TYPE_FUND = "xpath_//android.widget.CheckedTextView[@text='基金']"
# TRADE_TYPE="xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/lv_left']"
SWIPE_BEGIN = "swipe_xpath_//"
TRADE_TYPE_SCROLL = "swipe_xpath_//scroll_8"
COMPELETE_BUTTON = "xpath_//android.widget.TextView[@text='完成']"
CANCEL_BUTTON = "xpath_//android.widget.TextView[@text='取消']"

RECHARGE_SCROLL_1 = "swipe_xpath_//scroll_1"
WITHDRAW_SCROLL_1 = "swipe_xpath_//scroll_2"
SELECT_DONE = "id_com.shhxzq.xjb:id/tv_compeleted"

TRADE_TYPE = 'com.shhxzq.xjb:id/trade_type'
TRADE_DESC = 'com.shhxzq.xjb:id/trade_desp'
TRADE_STATUS = 'com.shhxzq.xjb:id/status'
TRADE_AMOUNT = 'com.shhxzq.xjb:id/trade_amount'


class XjbTradeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(XjbTradeDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def get_trade_record(self):
        type = str(self.get_text(TRADE_TYPE, 'find_element_by_id'))
        recharge_from = str(self.get_text(TRADE_DESC, 'find_element_by_id'))
        recharge_amount = str(self.get_text(TRADE_STATUS, 'find_element_by_id'))
        left_amount = str(self.get_text(TRADE_AMOUNT, 'find_element_by_id'))

        return type, recharge_from, recharge_amount, left_amount

    @robot_log
    def verify_trade_record_values(self, amount, operate_type=None):

        type = str(self.get_text(TRADE_TYPE, 'find_element_by_id'))
        specific_type = str(self.get_text(TRADE_DESC, 'find_element_by_id'))
        recharge_amount_actual = str(self.get_text(TRADE_STATUS, 'find_element_by_id'))
        left_amount = str(self.get_text(TRADE_AMOUNT, 'find_element_by_id'))

        if operate_type is None:
            self.assert_values('存入', type)
            self.assert_values('银行卡存入', specific_type)
            self.assert_values('+%.2f' % float(amount), recharge_amount_actual)

        elif operate_type == 'regular_withdraw':
            self.assert_values('取出', type)
            self.assert_values('普通取出', specific_type)
            self.assert_values('-%.2f' % float(amount), recharge_amount_actual)
        elif operate_type == 'fast_withdraw':
            self.assert_values('取出', type)
            self.assert_values('快速取出', specific_type)
            self.assert_values('-%.2f' % float(amount), recharge_amount_actual)

        self.assert_values('余额%.2f' % float(ASSERT_DICT['xjb_total_assets']), str(left_amount).replace(',', ''))

        page = self
        return page

