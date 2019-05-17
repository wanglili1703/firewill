# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log


class CreditCardRepayRecordPage(PageObject):
    def __init__(self, web_driver):
        super(CreditCardRepayRecordPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self, last_card_no):
        self.assert_values('工商银行', self.get_text('com.shhxzq.xjb:id/title_actionbar_fund', 'find_element_by_id'))
        last_card_no_text = self.get_text('com.shhxzq.xjb:id/title_actionbar_fundid', 'find_element_by_id')
        last_card_no_actual = filter(lambda ch: ch in '0123456789.', last_card_no_text)
        self.assert_values(last_card_no, last_card_no_actual)

        page = self
        return page

    @robot_log
    def verify_credit_card_repay_record_details(self, last_card_no, amount):
        last_card_no_text = self.get_text('com.shhxzq.xjb:id/trade_desp', 'find_element_by_id')
        last_card_no_actual = filter(lambda ch: ch in '0123456789.', last_card_no_text)
        amount_text = self.get_text('com.shhxzq.xjb:id/trade_amount', 'find_element_by_id')
        amount_actual = filter(lambda ch: ch in '0123456789.', amount_text)
        self.assert_values('信用卡还款', self.get_text('com.shhxzq.xjb:id/trade_type', 'find_element_by_id'))
        self.assert_values(last_card_no, last_card_no_actual)
        self.assert_values('成功', self.get_text('com.shhxzq.xjb:id/status', 'find_element_by_id'))
        self.assert_values('%.2f' % float(amount), amount_actual)

        page = self
        return page
