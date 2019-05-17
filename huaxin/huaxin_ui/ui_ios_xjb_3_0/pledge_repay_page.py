# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import re
from _common.global_config import ASSERT_DICT

import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page

AMOUNT = "//UIAStaticText[@label='还款本金']/following-sibling::UIATextField"
REPAY_AMOUNT = "xpathIOS_UIATextField_IOS%s" % AMOUNT
CONFIRM = "accId_UIAButton_(UIButton_还款)"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"


# SWIPE_BEGIN = "swipe_xpath_//"
# CONFIRM_SWIPE_STOP = "swipe_accId_还款"


class PledgeRepayPage(PageObject):
    def __init__(self, web_driver):
        super(PledgeRepayPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('随心还', self.get_text("//UIAStaticText[@label='随心还']"))

        page = self
        return page

    @robot_log
    def pledge_repay(self, pledge_repay_amount, trade_password):
        pledge_repay_amount_require_text = self.get_text(
            "//UIAStaticText[contains(@label, '最低还款本金为')]")

        pledge_repay_amount_min = float(
            re.findall(r'(\d{1,3}(,\d{3})*.\d+)', pledge_repay_amount_require_text)[0][0].replace(',', ''))
        pledge_repay_amount_threshold = float(
            re.findall(r'(\d{1,3}(,\d{3})*.\d+)', pledge_repay_amount_require_text)[1][0].replace(',', ''))
        interest_text = self.get_text("//UIAStaticText[@label='已产生利息(元)']/following-sibling::UIAStaticText")

        interest = '%.2f' % float(filter(lambda ch: ch in '0123456789.', interest_text))
        ASSERT_DICT.update({'interest': interest})

        self.perform_actions(REPAY_AMOUNT, pledge_repay_amount)
        # self.perform_actions(SWIPE_BEGIN, CONFIRM_SWIPE_STOP, 'U')
        self.perform_actions(CONFIRM)
        self.perform_actions(TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)
        return page
