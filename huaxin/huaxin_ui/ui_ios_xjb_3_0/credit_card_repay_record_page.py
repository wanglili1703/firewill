# coding: utf-8
import decimal

import huaxin_ui
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.credit_card_repay_page

LEFT_BUTTON = "accId_UIAButton_UIBarButtonItemLocationLeft"
current_page = []


class CreditCardRepayRecordPage(PageObject):
    def __init__(self, web_driver):
        super(CreditCardRepayRecordPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_back_to_credit_repay_page(self):
        self.perform_actions(LEFT_BUTTON)

        page = huaxin_ui.ui_ios_xjb_3_0.credit_card_repay_page.CreditCardRepayPage(self.web_driver)
        return page

    @robot_log
    def verify_at_repay_record_page(self):
        self.assert_values("还款记录", self.get_text("//UIAStaticText[@label='还款记录']"))

    @robot_log
    def verify_repay_record_details(self, last_card_no, bank, amount):
        self.assert_values("信用卡还款", self.get_text("(信用卡还款)", "find_element_by_accessibility_id"))
        self.assert_values("%s %s" % (bank, last_card_no),
                           self.get_text("(%s %s)" % (bank, last_card_no), "find_element_by_accessibility_id"))
        self.assert_values("成功", self.get_text("(成功)", "find_element_by_accessibility_id"))
        amount = decimal.Decimal(amount).quantize(decimal.Decimal('0.00'))
        self.assert_values("%s元" % amount, self.get_text("(%s元)" % amount, "find_element_by_accessibility_id"))
